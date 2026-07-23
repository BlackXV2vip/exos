#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌉 Exos Adapter — جسر OpenAI-Compatible لـ API بتاعك
=====================================================
يحوّل API البسيط (prompt/content) إلى صيغة OpenAI الكاملة:
  GET  /v1/models             → قائمة الموديلات
  POST /v1/chat/completions   → رد عادي أو SSE streaming
  + محاكاة tool calling عبر JSON-in-prompt للوكيل

التشغيل:  python3 exos_adapter.py [--port 8791]
"""
import json, re, sys, time, uuid, argparse, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import requests
from Crypto.Cipher import AES

# ═══════════════ الإعدادات ═══════════════
UPSTREAM_URL = "https://wormgpte.xo.je/agent_exos_api.php"
UPSTREAM_HOST = "wormgpte.xo.je"
MODEL_ID = "exos-1"
MODEL_NAME = "Exos Agent"
BROWSER_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
UPSTREAM_TIMEOUT = 150

# ═══════════════ إدارة جلسة الحماية (AES challenge) ═══════════════
class UpstreamSession:
    def __init__(self):
        self.lock = threading.Lock()
        self.session = None
        self._new_session()

    def _new_session(self):
        s = requests.Session()
        s.headers.update({"User-Agent": BROWSER_UA, "Accept": "*/*",
                          "Accept-Language": "en-US,en;q=0.9,ar;q=0.8"})
        self.session = s

    def solve_challenge(self, first_html=None):
        """حل تحدي AES بتاع الاستضافة (يدعم النسخة الـ raw والـ HTML-escaped)"""
        with self.lock:
            text = first_html
            url = UPSTREAM_URL
            for _ in range(8):
                if text is None:
                    try:
                        resp = self.session.get(url, timeout=30)
                    except requests.RequestException:
                        self._new_session()
                        continue
                    text = resp.text
                if "toNumbers(" not in text:
                    return  # مفيش تحدي — تمام
                try:
                    a = bytes.fromhex(re.search(r'a\s*=\s*toNumbers\("([a-f0-9]+)"\)', text).group(1))
                    b = bytes.fromhex(re.search(r'b\s*=\s*toNumbers\("([a-f0-9]+)"\)', text).group(1))
                    c = bytes.fromhex(re.search(r'c\s*=\s*toNumbers\("([a-f0-9]+)"\)', text).group(1))
                    cookie = AES.new(a, AES.MODE_CBC, b).decrypt(c).hex()
                    self.session.cookies.set("__test", cookie, domain=UPSTREAM_HOST)
                    nxt = re.search(r"location\.href\s*=\s*\"([^\"]+)\"", text).group(1)
                    url = nxt if nxt.startswith("https://") else f"https://{UPSTREAM_HOST}{nxt}"
                    text = None
                except Exception:
                    return

    def ask(self, prompt):
        """إرسال prompt وإرجاع الرد النصي (يكتشف التحدي بأي شكل)"""
        for attempt in range(4):
            try:
                r = self.session.post(UPSTREAM_URL, json={"prompt": prompt},
                                      timeout=UPSTREAM_TIMEOUT)
                if r.status_code == 403:
                    self.solve_challenge()
                    continue
                try:
                    data = r.json()
                except ValueError:
                    if "toNumbers(" in r.text:
                        self.solve_challenge(r.text)
                        continue
                    raise
                if data.get("ok"):
                    return data.get("content", ""), data.get("model", MODEL_ID)
                raise RuntimeError(data.get("error", "upstream error"))
            except (requests.RequestException, ValueError) as e:
                if attempt == 3:
                    raise
                self._new_session()
                time.sleep(1)

upstream = UpstreamSession()

# ═══════════════ تحويل صيغ الرسائل ═══════════════
TOOL_PREAMBLE = """You are running inside a code agent harness with tool access.
HARD RULES (violating them = total failure):
1. To act, output EXACTLY ONE raw JSON object and NOTHING else:
{"tool_calls":[{"name":"<tool>","arguments":{...}}]}
2. NEVER narrate, describe, or invent tool executions or results. Forbidden strings in your reply: "[tool result", "Done in", "<tool_calls>", "Move #", "✓".
3. NEVER write fake transcripts of yourself calling tools. The harness executes tools and shows real results by itself.
4. No markdown fences around the JSON. No text before or after it.
5. You may call multiple tools in the single tool_calls array.
If no action is needed, answer normally in plain text.
Available tools:
"""

def flatten_messages(messages):
    """تحويل سجل رسائل OpenAI إلى نص واحد"""
    parts = []
    for m in messages:
        role = m.get("role", "user")
        content = m.get("content", "")
        if isinstance(content, list):  # محتوى متعدد الأجزاء
            content = "\n".join(p.get("text", "") for p in content if isinstance(p, dict))
        if role == "tool":
            parts.append(f"[tool result ({m.get('name','tool')})]: {content}")
        elif role != "system":
            parts.append(f"{role}: {content}")
    return "\n".join(parts)

def build_prompt(messages, tools):
    sys_parts = [m.get("content", "") for m in messages if m.get("role") == "system"]
    prompt = ""
    if sys_parts:
        prompt += "\n".join(str(s) for s in sys_parts) + "\n\n"
    if tools:
        prompt += TOOL_PREAMBLE
        for t in tools:
            fn = t.get("function", {})
            desc = (fn.get("description") or "")[:200]
            params = json.dumps(fn.get("parameters", {}), ensure_ascii=False)[:600]
            prompt += f"- {fn.get('name')}: {desc} | args schema: {params}\n"
        prompt += "\n"
    prompt += flatten_messages(messages)
    return prompt

def extract_json_objects(src):
    """استخراج كائنات JSON متوازنة الأقواس من نص (يدعم التداخل والسترنچات)"""
    objs, depth, start, in_str, esc = [], 0, -1, False, False
    for i, ch in enumerate(src):
        if in_str:
            if esc: esc = False
            elif ch == "\\": esc = True
            elif ch == '"': in_str = False
            continue
        if ch == '"': in_str = True
        elif ch == "{":
            if depth == 0: start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start >= 0:
                objs.append(src[start:i+1]); start = -1
    return objs

def to_openai_call(name, args):
    return {"id": f"call_{uuid.uuid4().hex[:8]}", "type": "function",
            "function": {"name": name, "arguments": json.dumps(args, ensure_ascii=False)}}

def parse_tool_calls(text):
    """محاولة استخراج tool call من رد الموديل"""
    t = text.strip()
    # صيغة <tool_calls> كائنات JSON متتالية
    if "<tool_calls>" in t:
        chunk = t.split("<tool_calls>", 1)[1].split("</tool_calls>", 1)[0]
        calls = []
        for raw in extract_json_objects(chunk):
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if obj.get("name"):
                calls.append(to_openai_call(obj["name"], obj.get("arguments", {})))
        if calls:
            return calls
    t = text.strip()
    t = re.sub(r"^```(?:json)?|```$", "", t, flags=re.M).strip()
    candidates = [t]
    m = re.search(r"\{.*\"tool_calls\".*\}", t, re.DOTALL)
    if m:
        candidates.insert(0, m.group(0))
    for cand in candidates:
        try:
            obj = json.loads(cand)
            calls = obj.get("tool_calls")
            if isinstance(calls, list) and calls and calls[0].get("name"):
                return [{"id": f"call_{uuid.uuid4().hex[:8]}", "type": "function",
                         "function": {"name": c["name"],
                                      "arguments": json.dumps(c.get("arguments", {}), ensure_ascii=False)}}
                        for c in calls]
        except (json.JSONDecodeError, AttributeError, IndexError):
            continue
    return None

# ═══════════════ صيغ OpenAI ═══════════════
def completion_body(text, tool_calls, model):
    msg = {"role": "assistant", "content": None if tool_calls else text}
    if tool_calls:
        msg["tool_calls"] = tool_calls
    return {
        "id": f"chatcmpl-{uuid.uuid4().hex[:20]}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [{"index": 0,
                     "finish_reason": "tool_calls" if tool_calls else "stop",
                     "message": msg}],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    }

def sse_chunks(text, tool_calls, model):
    """تقسيم الرد إلى SSE chunks (يمّل streaming حتى لو المصدر غير متدفق)"""
    cid = f"chatcmpl-{uuid.uuid4().hex[:20]}"
    def chunk(delta, finish=None):
        return ("data: " + json.dumps({
            "id": cid, "object": "chat.completion.chunk",
            "created": int(time.time()), "model": model,
            "choices": [{"index": 0, "delta": delta, "finish_reason": finish}]},
            ensure_ascii=False) + "\n\n").encode()
    yield chunk({"role": "assistant", "content": ""})
    if tool_calls:
        tc = tool_calls[0]
        args = tc["function"]["arguments"]
        yield chunk({"tool_calls": [{"index": 0, "id": tc["id"], "type": "function",
                                     "function": {"name": tc["function"]["name"], "arguments": ""}}]})
        for i in range(0, len(args), 32):
            yield chunk({"tool_calls": [{"index": 0, "function": {"arguments": args[i:i+32]}}]})
        yield chunk({}, "tool_calls")
    else:
        # تقسيم النص كلمات كلمات (شكل streaming طبيعي)
        words = re.findall(r"\S+\s*|\s+", text)
        buf, count = "", 0
        for w in words:
            buf += w; count += 1
            if count % 6 == 0:
                yield chunk({"content": buf}); buf = ""
        if buf:
            yield chunk({"content": buf})
        yield chunk({}, "stop")
    yield b"data: [DONE]\n\n"

# ═══════════════ السيرفر ═══════════════
class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    def log_message(self, fmt, *a):
        sys.stderr.write(f"  ⬅ {self.command} {self.path}\n")

    def _json(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.rstrip("/")
        if path.endswith("/api.json"):
            # كتالوج بصيغة models.dev — الوكيل يكتشفنا تلقائياً عبر EXOS_AGENT_MODELS_URL
            self._json({
                "exos": {
                    "id": "exos", "name": MODEL_NAME,
                    "api": f"http://127.0.0.1:{self.server.server_port}/v1",
                    "env": [],
                    "models": {
                        MODEL_ID: {
                            "id": MODEL_ID, "name": MODEL_NAME,
                            "family": "exos", "tool_call": True,
                            "reasoning": False, "attachment": False,
                            "temperature": True,
                            "cost": {"input": 0, "output": 0},
                            "limit": {"context": 128000, "output": 8192},
                        }
                    },
                }
            })
        elif path.endswith("/models"):
            self._json({"object": "list", "data": [{
                "id": MODEL_ID, "object": "model",
                "created": int(time.time()), "owned_by": "exos-agent"}]})
        else:
            self._json({"ok": True, "name": "Exos Adapter", "model": MODEL_ID})

    def do_POST(self):
        if "chat/completions" not in self.path:
            return self._json({"error": "not found"}, 404)
        try:
            length = int(self.headers.get("Content-Length", 0))
            req = json.loads(self.rfile.read(length) or b"{}")
        except Exception:
            return self._json({"error": "bad json"}, 400)

        messages = req.get("messages", [])
        tools = req.get("tools") or []
        want_stream = bool(req.get("stream"))
        t0 = time.time()
        print(f"  📨 طلب: {len(messages)} رسالة | أدوات: {len(tools)} | stream: {want_stream}", file=sys.stderr)

        try:
            text, _model = upstream.ask(build_prompt(messages, tools))
        except Exception as e:
            return self._json({"error": {"message": str(e), "type": "UpstreamError"}}, 502)

        tool_calls = parse_tool_calls(text)
        dt = time.time() - t0
        print(f"  ✅ رد في {dt:.1f}s | tool_call: {'نعم:' + tool_calls[0]['function']['name'] if tool_calls else 'لا'}", file=sys.stderr)

        if not want_stream:
            return self._json(completion_body(text if not tool_calls else None, tool_calls, MODEL_ID))

        body = b"".join(sse_chunks(text, tool_calls, MODEL_ID))
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8791)
    args = ap.parse_args()
    print(f"🌉 Exos Adapter شغال على http://127.0.0.1:{args.port}/v1")
    print(f"   المصدر: {UPSTREAM_URL}")
    ThreadingHTTPServer(("127.0.0.1", args.port), Handler).serve_forever()
