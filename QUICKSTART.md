# 🚀 تجربة Exos Agent في 5 دقائق | Try Exos Agent in 5 Minutes

<p align="center">
  <img src="assets/banner.png" alt="Exos Agent" width="100%">
</p>

> كل الخطوات دي **متجربة فعليًا** على النسخة المنشورة — انسخ والصق وهيشتغل ✅
> Every step below was **actually executed and verified** against the published release.

---

## ⚡ الطريقة السريعة — أمر واحد | The fast way — one command

```bash
curl -fsSL https://raw.githubusercontent.com/BlackXV2vip/exos/main/install | bash
```

- 🇪🇬 المثبّت بيعمل كل حاجة لوحده: ينزّل الباينري ويتحقق من SHA256، يسطّبه في `~/.local/bin`، يسطّب مكتبات الجسر، ينزّل الجسر والكونفيج الجاهز، ويعمل أمر `exos-bridge`. بعدها: `exos-bridge` في تيرمينال و `exos-agent chat` في تيرمينال تاني 🎉
- 🇬🇧 The installer does everything: downloads the latest binary (SHA256-verified) to `~/.local/bin`, installs bridge dependencies, fetches the bridge + ready config, and creates an `exos-bridge` command. Then run `exos-bridge` in one terminal and `exos-agent chat` in another.

### 🔄 التحديث لإصدار أحدث | Updating

```bash
# من أي إصدار — نفس الأمر بيحدّثك لآخر ريليز (الكونفيج والجسر بيفضلوا زي ما هما)
curl -fsSL https://raw.githubusercontent.com/BlackXV2vip/exos/main/install | bash

# من v1.18.6 وفايت — التحديث المدمج شغال:
exos-agent upgrade
```

*From any version, re-running the installer updates you to the latest release (your config & bridge stay untouched). From v1.18.6 onward, the built-in `exos-agent upgrade` command works too.*

---

> 🖥️ المنصات المدعومة: Linux **x86_64** و Linux **ARM64** — يعني شغال على الموبايل بـ Termux/proot كمان! الدليل: **[TERMUX.md](TERMUX.md)** 📱
> Supported platforms: Linux **x86_64** & **ARM64** — yes, it runs on Android via Termux/proot! Guide: **[TERMUX.md](TERMUX.md)** 📱

> 📋 عايز تعملها بإيدك خطوة خطوة؟ كمّل تحت | Want to do it manually, step by step? Continue below.

---

## 🇪🇬 بالعربي

### المتطلبات

| المتطلب | الأمر للتأكد |
|---|---|
| Linux x86_64 (أو macOS عبر بناء من المصدر) | `uname -m` → `x86_64` |
| Python 3.8+ (للجسر المجاني فقط) | `python3 --version` |
| `curl` و `tar` | موجودين افتراضيًا في أغلب التوزيعات |

### الخطوة 1 — حمّل الباينري من الـ Release

```bash
curl -L -o exos-agent.tar.gz \
  https://github.com/BlackXV2vip/exos/releases/download/v1.18.7/exos-agent-linux-x64.tar.gz

# (اختياري) تأكد من سلامة الملف — لازم يطلع نفس الهاش ده:
sha256sum exos-agent.tar.gz
# 717d514647ee106a1b9cf4574e31d24c68fccd4486776d58c76933f8760adf30
```

### الخطوة 2 — فك الضغط وشغّل

```bash
tar xzf exos-agent.tar.gz        # بيطلع ملف واحد اسمه exos-agent
chmod +x exos-agent
./exos-agent --version           # ✅ المفروض يطبع: 1.18.7
```

> حبيت تخليه أمر عام؟ `sudo mv exos-agent /usr/local/bin/`

### الخطوة 3 — شغّل الجسر المجاني (Exos Adapter)

الوكيل بيشتغل مع أي مزوّد OpenAI-compatible، وجاهز معاه **جسر مجاني مدمج** (`exos_adapter.py` من الريبو):

```bash
pip3 install requests pycryptodome
python3 exos_adapter.py
# ✅ المفروض تشوف: 🌉 Exos Adapter شغال على http://127.0.0.1:8791/v1
```

> ⚠️ سيب الترمينال ده مفتوح — ده الجسر اللي الوكيل بيتكلم من خلاله.

### الخطوة 4 — جهّز الكونفيج (مرة واحدة بس)

```bash
mkdir -p ~/.config/exos-agent
cp examples/exos-agent.json ~/.config/exos-agent/exos-agent.json
```

أو الصق ده بنفسك في `~/.config/exos-agent/exos-agent.json`:

```json
{
  "$schema": "https://exos-agent.ai/config.json",
  "provider": {
    "exos": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Exos Agent",
      "options": { "baseURL": "http://127.0.0.1:8791/v1", "apiKey": "public" },
      "models": { "exos-1": { "name": "Exos Agent", "tools": true } }
    }
  },
  "model": "exos/exos-1",
  "small_model": "exos/exos-1"
}
```

### الخطوة 5 — جرّب 🎉

```bash
# شات تفاعلي — اسأل وهو يرد وينفّذ (اكتب /exit للخروج)
./exos-agent chat

# مهمة تنفيذية مباشرة — بيكتب ملفات ويشغّل أوامر لوحده
./exos-agent run "create hello.py that prints fibonacci and run it"

# الواجهة الكاملة TUI
./exos-agent
```

> 💡 أول طلب ممكن ياخد 10–60 ثانية (الجسر بيحل تحدي حماية مع السيرفر المجاني) — بعدها بيمشي طبيعي.

### حل المشاكل

| المشكلة | الحل |
|---|---|
| `Connection refused` على 8791 | الجسر مش شغال → ارجع للخطوة 3 |
| أول رد بطيء جدًا | طبيعي — تحدي الحماية بيتحل مرة واحدة لكل جلسة |
| `No module named 'Crypto'` | `pip3 install pycryptodome` |
| عايز مزوّد تاني (OpenAI/محلي/أي OpenAI-compatible) | غيّر `baseURL` و `apiKey` في الكونفيج — مش محتاج الجسر |

---

## 🇬🇧 English

### Requirements
Linux **x86_64**, and Python 3.8+ (only for the included free bridge).

### 1 — Download the release binary

```bash
curl -L -o exos-agent.tar.gz \
  https://github.com/BlackXV2vip/exos/releases/download/v1.18.7/exos-agent-linux-x64.tar.gz

# (optional) verify integrity — must print:
sha256sum exos-agent.tar.gz
# 717d514647ee106a1b9cf4574e31d24c68fccd4486776d58c76933f8760adf30
```

### 2 — Extract & smoke-test

```bash
tar xzf exos-agent.tar.gz        # yields a single file: exos-agent
chmod +x exos-agent
./exos-agent --version           # ✅ prints: 1.18.7
```

### 3 — Start the free bridge (Exos Adapter)

Exos Agent works with **any OpenAI-compatible provider**. A free ready-made bridge ships in this repo:

```bash
pip3 install requests pycryptodome
python3 exos_adapter.py          # serves http://127.0.0.1:8791/v1 — keep it open
```

### 4 — One-time config

```bash
mkdir -p ~/.config/exos-agent
cp examples/exos-agent.json ~/.config/exos-agent/exos-agent.json
```

### 5 — Try it 🎉

```bash
./exos-agent chat                                  # interactive chat (/exit to quit)
./exos-agent run "create hello.py and run it"      # one-shot agentic task
./exos-agent                                       # full TUI
```

> 💡 The first request may take 10–60s while the bridge solves the upstream security challenge. Subsequent requests are much faster.

### Troubleshooting

| Symptom | Fix |
|---|---|
| `Connection refused` on 8791 | Bridge isn't running → step 3 |
| Very slow first reply | Expected — one-time challenge solve per session |
| `No module named 'Crypto'` | `pip3 install pycryptodome` |
| Want another provider (OpenAI/local/any OpenAI-compatible) | Edit `baseURL` + `apiKey` in the config — no bridge needed |

---

## ✅ Verified live (2026-07-23 — v1.18.7)

| Check | Result |
|---|---|
| 🌐 **Web UI embedded & served** from the binary | ✅ `exos-agent serve` → `<title>Exos Agent</title>` |
| `serve` command branding | ✅ "starts a headless exos-agent server" |
| `exos-agent --version` — Linux **x64** | ✅ `1.18.7` |
| `exos-agent --version` — Linux **ARM64** (via qemu) | ✅ `1.18.7` |
| Zero legacy-name strings in **both** binaries | ✅ 0 occurrences |
| **One-command installer** (`curl\|bash`) end-to-end | ✅ binary + bridge + config + `exos-bridge` (tested x64 & aarch64) |
| Installer's automatic SHA256 verification | ✅ "الهاش مطابق — الملف أصلي" |
| Real agentic task on the release binary | ✅ wrote `v.txt` → exact content |
| Interactive `chat` session memory (2 turns, Arabic) | ✅ remembered the user's name in 2.6s |
| Web UI «New session» on a **fresh server without projects** (the bug reported by the user) | ✅ fixed in v1.18.7 — navigates to composer instantly (Playwright E2E) |
| Web UI full chat loop in Arabic (send → reply) | ✅ «قولي ازيك» ← «أنا بخير» in 6s, auto Arabic session title |

> المزيد من اختبارات الأدوات الصعبة: [TESTING.md](TESTING.md)

---

## 💬 محتاج مساعدة؟ | Need help?

| | |
|---|---|
| 📢 قناة التليجرام — تحديثات ودعم | 👉 [t.me/HackerExos_VIP](https://t.me/HackerExos_VIP) |
| 👨‍💻 المطور مباشرة | 👉 [@HackerExos](https://t.me/HackerExos) |
