# 🎯 SAML CTF - IMMEDIATE ACTION PLAN

## ⚡ Do This NOW (5 Minutes to Flag)

### Step 1: Open Browser & Login
```
URL: https://saml-web.challs.infobahnc.tf
Username: sahas
Password: 123
```

### Step 2: Get Session Cookie
1. Press `F12` (DevTools)
2. Go to `Application` tab → `Cookies` (left sidebar)
3. Click on `https://saml-web.challs.infobahnc.tf`
4. Find `authentik_session` 
5. **Double-click the Value column** and copy (Ctrl+C)

### Step 3: Run Exploit
Open PowerShell in this folder and run:

```powershell
node authentik_api.js --target https://saml-web.challs.infobahnc.tf --session "authentik_session=PASTE_HERE"
```

**Replace `PASTE_HERE` with the value you copied!**

### Step 4: Get Flag
If exploit succeeds, visit:
```
https://saml-web.challs.infobahnc.tf/flag
```

---

## 🚨 What Each Tool Does

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `authentik_api.js` | **THE EXPLOIT** - Creates malicious SAML mapping | Use this to solve the challenge |
| `saml_decoder.js` | Decodes SAML responses to see what username is sent | Debugging / verification |
| `cookie_helper.js` | Helps format cookies correctly | If you're confused about cookies |

---

## 🎯 Expected Exploit Flow

```
You → Login as sahas → Get cookie
  ↓
Run authentik_api.js with cookie
  ↓
Tool creates mapping: "always return akadmin"
  ↓
Tool injects mapping into flaggetter provider
  ↓
You → Visit /flag → IdP redirects for auth
  ↓
You → Login again as sahas
  ↓
IdP uses YOUR malicious mapping
  ↓
SAML response contains: username="akadmin"
  ↓
Flaggetter app sees: username === "akadmin" ✓
  ↓
🏁 FLAG DISPLAYED!
```

---

## ❓ Troubleshooting

### "Cannot find module 'xmldom'"
```powershell
npm install xmldom
```

### "403 Forbidden" or "401 Unauthorized"
Your cookie expired. Re-login and get a fresh one.

### "No flaggetter provider found"
The provider might have a different name. Check manually:
```powershell
# In browser, logged in as sahas, visit:
https://saml-web.challs.infobahnc.tf/api/v3/providers/saml/
```

### Still shows "not authorized"
Decode the SAML response to see what username is actually sent:
```powershell
# 1. Visit /flag, copy SAMLResponse parameter from URL
# 2. Decode it:
node saml_decoder.js "H4sIAAAA_PASTE_SAMLRESPONSE_HERE_..."
```

If it shows username="sahas", the mapping wasn't applied. Try:
- Remove all other username mappings from provider
- Put your malicious mapping FIRST in the list

---

## 🎓 Why This Works (Quick Version)

The app checks: **"Is username in SAML assertion equal to akadmin?"**

But it doesn't check: **"Is the authenticated user actually akadmin?"**

So if we can control what username goes INTO the SAML assertion, we win!

Normal users can't sign SAML (need private key). BUT if Authentik lets regular users create property mappings, we can control what the IdP puts in the assertion BEFORE signing.

Think of it like:
- IdP is a trusted notary
- They sign documents saying "This person is X"
- If YOU can tell the notary what to write, you can get them to sign "This person is akadmin" even though you're really sahas!

---

## 📊 Quick Reference

### Files You Need
```
saml/
├── authentik_api.js    ← THE EXPLOIT
├── saml_decoder.js     ← Debugging tool
├── cookie_helper.js    ← Cookie formatting
├── QUICKSTART.md       ← You are here!
└── README.md           ← Full documentation
```

### Commands You Need
```powershell
# Install dependencies (once)
npm install xmldom

# Run exploit (with your cookie)
node authentik_api.js --target https://saml-web.challs.infobahnc.tf --session "authentik_session=YOUR_COOKIE"

# Decode SAML response (for debugging)
node saml_decoder.js "BASE64_SAML_RESPONSE"

# Test cookie validity
$headers = @{ "Cookie" = "authentik_session=YOUR_COOKIE" }
Invoke-RestMethod -Uri "https://saml-web.challs.infobahnc.tf/api/v3/core/users/me/" -Headers $headers
```

---

## ✅ Success Checklist

Before running exploit:
- [ ] Logged into https://saml-web.challs.infobahnc.tf as sahas/123
- [ ] Copied `authentik_session` cookie value
- [ ] Installed xmldom (`npm install xmldom`)

After running exploit:
- [ ] Tool says "Provider updated successfully!"
- [ ] No error messages
- [ ] Visited /flag endpoint
- [ ] Logged in again when redirected to IdP
- [ ] Flag displayed!

---

## 🏁 Final Notes

- This should take **under 5 minutes** once you have the cookie
- The vulnerability is a **configuration issue**, not a crypto break
- In real life, this would be **critical severity** - regular users controlling identity claims!
- The signature verification is actually **done correctly** - we're just exploiting trust boundaries

**Good luck! 🚀**

---

*Need detailed explanation of attack vectors? See `EXPLOIT_GUIDE.md`*  
*Need full background and theory? See `README.md`*  
*Having issues? Check the Troubleshooting section above!*
