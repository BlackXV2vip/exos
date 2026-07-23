# 📱 تشغيل Exos Agent على أندرويد (Termux) | Run Exos Agent on Android

> عندنا باينري رسمي **ARM64 (aarch64) glibc** من إصدار v1.18.6 — مصمم يشتغل جوه **proot-distro (Debian/Ubuntu)** على الموبايل.
> We ship an official **ARM64 (aarch64) glibc** binary since v1.18.6 — built to run inside **proot-distro (Debian/Ubuntu)** on Android.

---

## 🇪🇬 بالعربي — خطوة بخطوة من الصفر

### المتطلبات
- موبايل أندرويد بمعالج 64-bit (أغلب الموبايلات من 2016 وطلعت)
- تطبيق **Termux** — حمّله من **F-Droid** أو **GitHub** (نسخة Google Play قديمة وبتعمل مشاكل، متستهلهاش)
- نت ثابت أول مرة (تحميلات ~120MB)

### 1️⃣ جهّز ترمكس ودبيان

```bash
# جوه ترمكس نفسه
pkg update -y && pkg upgrade -y
pkg install -y proot-distro tmux
proot-distro install debian
```

> 💡 عندك دبيان متسطّبة من قبل كده؟ عدّي الخطوة دي على طول.

### 2️⃣ ادخل جوه دبيان

```bash
proot-distro login debian
```

### 3️⃣ جهّز الأدوات (مرة واحدة بس)

```bash
apt update -y && apt install -y curl python3 python3-pip ca-certificates tmux
```

### 4️⃣ الأمر السحري 🪄

```bash
curl -fsSL https://raw.githubusercontent.com/BlackXV2vip/exos/main/install | bash
```

المثبّت **بيكتشف إنك على ARM64 تلقائي** وبينزّل النسخة الصح، بيتحقق من الهاش، وبيجهزلك كل حاجة ✅

```bash
# بعد التثبيت:
export PATH="$HOME/.local/bin:$PATH"   # أو اقفل وافتح proot من جديد
exos-agent --version                    # ✅ المفروض يطبع: 1.18.6
```

### 5️⃣ التشغيل (بـ tmux — أريح طريقة على الموبايل)

```bash
tmux new -s exos
# في أول نافذة: شغّل الجسر
exos-bridge
# اعمل نافذة تانية: Ctrl+b وبعدين حرف c
# في النافذة التانية: شغّل الوكيل
exos-agent chat
```

التنقل بين النوافذ: `Ctrl+b` وبعدين `0` أو `1` — والخروج من tmux من غير ما تقفل حاجة: `Ctrl+b` وبعدين `d`.

> ⚠️ أول رد من الوكيل ممكن ياخد 10–60 ثانية (الجسر بيحل تحدي حماية مرة واحدة) — بعدها سريع.

### 🌐 الواجهة الويب على الموبايل (v1.18.6+)

الباينري جواه واجهة ويب كاملة مدمجة — شغّلها في نافذة tmux لوحدها:

```bash
# خلّي الجسر شغال في نافذة، وفي نافذة تانية:
exos-agent serve --port 8799
# يطبع: exos-agent server listening on http://127.0.0.1:8799
```

وبعدين افتح متصفح الموبايل (كروم/فايرفوكس) على:

```
http://127.0.0.1:8799
```

هتلاقي واجهة Exos Agent كاملة شغالة من موبايلك مباشرة 📱🔥
*(The v1.18.6+ binary embeds the full web UI — serve it and open your phone browser at the address above.)*

### 🔄 تحديث الأداة بعدين

```bash
# نفس أمر التثبيت — بيجيب أحدث إصدار ويحدّث الباينري في مكانه
# (الكونفيج والجسر والجلسات بيفضلوا زي ما هما)
curl -fsSL https://raw.githubusercontent.com/BlackXV2vip/exos/main/install | bash

# ومن v1.18.6 وفايت — بقى فيه أمر مدمج:
exos-agent upgrade
```

### 🛠️ حل المشاكل الشائعة على ترمكس

| المشكلة | السبب | الحل |
|---|---|---|
| `Exec format error` | شغّلت نسخة x64 على موبايل ARM | المثبّت الجديد بيحلها تلقائي — نزّل رابط التثبيت |
| `pip: command not found` | دبيان ناقصها pip | `apt install -y python3-pip` |
| `externally-managed-environment` | دبيان بتقفل pip العادي | المثبّت بيعالجها أوتوماتيك؛ يدويًا ضيف `--break-system-packages` |
| `certificate verify failed` | شهادات ناقصة | `apt install -y ca-certificates && update-ca-certificates` |
| الوكيل بطيء أول مرة | تحدي الحماية للسيرفر المجاني | طبيعي — مرة واحدة لكل جلسة جسر |
| قطعت النت/قفلت الترمكس | الجلسة ماتت | شغّل tmux من جوه proot عشان الجلسة تفضل عايشة |
| مساحة التخزين | الباينري ~150MB بعد الفك | اتأكد إن عندك 500MB فاضين في الموبايل |

### 💡 نصايح للموبايل

- **سِب الجسر شغال في tmux** — كده مفيش تحدي حماية جديد كل شوية.
- لو عايز توصل لملفات الموبايل: `termux-setup-storage` في ترمكس، وبعدين من proot هتلاقيها في `/sdcard`.
- ارجع تاني أي وقت: `proot-distro login debian` — كل حاجة محفوظة.

---

## 🇬🇧 English — from zero

```bash
# in Termux itself (F-Droid/GitHub build, not the stale Google Play one)
pkg update -y && pkg upgrade -y
pkg install -y proot-distro tmux
proot-distro install debian
proot-distro login debian

# inside Debian — one-time deps
apt update -y && apt install -y curl python3 python3-pip ca-certificates tmux

# the magic one-liner 🪄 (auto-detects ARM64)
curl -fsSL https://raw.githubusercontent.com/BlackXV2vip/exos/main/install | bash
export PATH="$HOME/.local/bin:$PATH"

# run (tmux = comfy on mobile)
tmux new -s exos
exos-bridge          # window 0 — keep alive
# Ctrl+b then c → new window
exos-agent chat      # window 1 — talk to your agent 🎉
```

> The prebuilt ARM64 binary is **glibc** — that's why it runs inside proot Debian/Ubuntu, not in raw Termux (Bionic). This is expected; proot-distro is the supported path.

---

## ✅ متجرب على ARM64 | Verified on ARM64

| التحقق Check | النتيجة Result |
|---|---|
| بناء باينري `linux-arm64` من المصدر | ✅ `ELF 64-bit ARM aarch64, glibc` |
| تشغيل فعلي على معمارية ARM64 (محاكي qemu) | ✅ `--version` → `1.18.6` |
| المثبّت بيكتشف aarch64 وينزّل نسخة الموبايل | ✅ مكتشف تلقائي |
| صفر آثار لأي اسم قديم في باينري ARM64 | ✅ 0 |
| 🌐 الواجهة الويب مدموجة ومسحوبة من الباينري نفسه | ✅ `<title>Exos Agent</title>` |

---

## 💬 محتاج مساعدة؟ | Need help?

| | |
|---|---|
| 📢 قناة التليجرام | 👉 [t.me/HackerExos_VIP](https://t.me/HackerExos_VIP) |
| 👨‍💻 المطور مباشرة | 👉 [@HackerExos](https://t.me/HackerExos) |
