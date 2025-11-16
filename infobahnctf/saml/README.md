# SAML CTF Challenge - Complete Solution Kit

## 🎯 Challenge Summary
- **Name**: SAML (480 points)
- **URL**: https://saml-web.challs.infobahnc.tf
- **Objective**: Obtain flag by authenticating as `akadmin` via SAML
- **Current Access**: Regular user account (sahas/123)

---

## 📁 Files in This Kit

| File | Purpose |
|------|---------|
| `QUICKSTART.md` | **START HERE** - Fast track to exploitation |
| `EXPLOIT_GUIDE.md` | Detailed vulnerability analysis and attack vectors |
| `authentik_api.js` | Automated exploit tool for property mapping injection |
| `saml_decoder.js` | SAML response decoder and analyzer |
| `saml-handout/` | Challenge source code (reference) |

---

## 🚀 Quick Exploitation Path

### 1️⃣ Install Dependencies
```powershell
npm install xmldom
```

### 2️⃣ Get Session Cookie
1. Login to https://saml-web.challs.infobahnc.tf as `sahas` / `123`
2. Open DevTools (F12) → Application → Cookies
3. Copy `authentik_session` value

### 3️⃣ Run Automated Exploit
```powershell
node authentik_api.js `
  --target https://saml-web.challs.infobahnc.tf `
  --session "authentik_session=YOUR_COOKIE_VALUE_HERE"
```

### 4️⃣ Retrieve Flag
Visit: https://saml-web.challs.infobahnc.tf/flag

---

## 🔍 How the Exploit Works

### Vulnerability: Property Mapping Privilege Escalation

**The Issue:**
- The application trusts SAML assertions signed by the IdP (Authentik)
- Regular users can create/modify SAML property mappings
- Mappings control what attributes (including username) are included in SAML assertions
- No proper RBAC enforcement on mapping creation

**The Attack:**
1. Create a malicious SAML property mapping that returns static value `akadmin`
2. Inject this mapping into the `flaggetter` SAML provider
3. Next authentication → SAML contains `username=akadmin`
4. Application checks: `if (username === 'akadmin')` → **TRUE** → Flag revealed!

### Code Analysis (from index.js)

```javascript
// Username extracted from SAML attribute
const username = xmlDoc.querySelector(
    'Attribute[Name="http://schemas.goauthentik.io/2021/02/saml/username"] AttributeValue'
)?.textContent;

// Simple string comparison - no additional checks!
if ( username === 'akadmin' ) {
    res.type( 'text/plain' ).send( process.env.FLAG || 'flag{fake}' );
}
```

**Security measures that ARE present:**
- ✅ XML signature verification (using xml-crypto)
- ✅ Constraint on signature structure (no wrapper attacks)
- ✅ Transform limit (max 2 transforms)
- ✅ Reference URI validation

**What's MISSING:**
- ❌ No verification that username matches authenticated user
- ❌ Trust assumption: "If IdP says username=X, then user IS X"
- ❌ No check for privileged attributes needing extra validation

**Root Cause:**
The app assumes only admins can control SAML attribute mappings. In reality, Authentik's default RBAC may allow regular users to create mappings, breaking this trust assumption.

---

## 🛠️ Tools Documentation

### authentik_api.js - Automated Exploitation

**What it does:**
1. Authenticates with your session cookie
2. Creates a property mapping: `return "akadmin"`
3. Finds the flaggetter SAML provider
4. Injects malicious mapping into provider config
5. Next SAML auth uses tampered username

**Usage:**
```powershell
node authentik_api.js --target <url> --session <cookie>
```

**Output Example:**
```
✓ Logged in as: sahas (Sahas User)
✓ Created mapping ID: abc-123-def
✓ Found provider: flaggetter (ID: xyz-789)
✓ Provider updated successfully!

📝 Next steps:
   1. Visit: https://saml-web.challs.infobahnc.tf/flag
   2. Flag should be displayed!
```

---

### saml_decoder.js - Response Analyzer

**What it does:**
- Base64 decodes SAMLResponse parameter
- Decompresses (inflateRaw)
- Parses and pretty-prints XML
- Extracts key info: username, signatures, transforms
- Performs security checks

**Usage:**
```powershell
# Direct base64 input
node saml_decoder.js "H4sIAAAAAAAA..."

# From URL
node saml_decoder.js --from-url "https://example.com/flag?SAMLResponse=..."
```

**When to use:**
- Verify malicious username appears in SAML
- Debug why exploit isn't working
- Understand SAML structure before crafting attacks

---

## 🎓 Alternative Attack Vectors (If Primary Fails)

### Option A: Username Registration Tricks
Try creating accounts with:
- `akadmin` (direct - likely blocked)
- `Akadmin` / `AKADMIN` (case variations)
- `akadmin ` (trailing space)
- Unicode lookalikes: `аkadmin` (Cyrillic а)

### Option B: Password Recovery Exploitation
- Try "Forgot Password" for `akadmin`
- Enumerate email if exposed
- Check for weak reset token generation

### Option C: SAML XML Signature Bypass (Advanced)
- XPath transform abuse (narrow signed subset)
- Signature wrapping (unlikely given code constraints)
- Comment injection in attributes

### Option D: Direct API Manipulation
If you can't create mappings via API, try:
- Forging JWT tokens (if found in responses)
- Session fixation/hijacking
- Exploiting other Authentik flows

---

## 🐛 Troubleshooting

### Error: "403 Forbidden" on API calls
**Cause:** Insufficient permissions or bad session
**Fix:**
- Re-login and get fresh cookie
- Check if `is_staff` or `is_superuser` flags set
- Try accessing `/if/admin/` manually in browser

### Error: "No flaggetter provider found"
**Cause:** Provider name different or search failed
**Fix:**
- List all providers: `GET /api/v3/providers/saml/`
- Check actual name in response
- Update search term in script

### Flag still shows "not authorized"
**Cause:** Mapping not applied or overridden
**Fix:**
- Decode SAMLResponse to verify username
- Check if multiple username mappings exist
- Remove competing mappings
- Clear browser cache / use incognito

### TypeError: Cannot read property...
**Cause:** Missing dependency
**Fix:**
```powershell
npm install xmldom
```

---

## 📚 Learning Resources

### SAML Security Basics
- [SAML Security Cheat Sheet (OWASP)](https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html)
- [XML Signature Wrapping Attacks](https://www.usenix.org/system/files/conference/usenixsecurity12/sec12-final91.pdf)
- [Authentik Documentation](https://goauthentik.io/docs/)

### Similar CTF Challenges
- PicoCTF: SAML challenges
- HackTheBox: SSO/SAML machines
- PortSwigger Web Academy: OAuth/SAML labs

---

## 🎉 Success Checklist

- [ ] Dependencies installed (`xmldom`)
- [ ] Session cookie extracted from browser
- [ ] `authentik_api.js` executed without errors
- [ ] Property mapping created (check API response)
- [ ] Provider updated with malicious mapping
- [ ] Visited `/flag` endpoint after re-authentication
- [ ] Flag displayed on screen
- [ ] Flag submitted to CTF platform

---

## 💡 Key Takeaways

### For CTF Players
1. **Trust boundaries matter**: Even with perfect crypto, misplaced trust breaks security
2. **RBAC is critical**: Who can modify identity claims?
3. **Defense in depth**: Signature verification isn't enough alone
4. **API enumeration**: Always check if APIs enforce UI permissions

### For Developers
1. **Never trust attributes blindly**: Even from signed assertions
2. **Implement proper RBAC**: Critical configs should require admin privileges
3. **Validate privileged claims**: Username/role attributes need extra checks
4. **Audit trail**: Log who modifies attribute mappings

### For Security Engineers
1. **Test RBAC exhaustively**: Can regular users access admin functions?
2. **Review trust assumptions**: Document what each component trusts
3. **Signature != Authorization**: Crypto proves authenticity, not authorization
4. **Configuration hardening**: Disable self-service for critical settings

---

## 📞 Need Help?

### Debug Steps
1. Run decoder on captured SAML response
2. Check API responses for error messages
3. Verify session cookie is valid (test with `/api/v3/core/users/me/`)
4. Review browser console for JS errors

### Common Questions
**Q: Can I use Burp Suite instead of Node.js tools?**
A: Yes! The APIs are standard REST - just add session cookie to requests.

**Q: Do I need the local docker-compose environment?**
A: No, everything can be done against the remote challenge instance.

**Q: What if I don't have admin privileges?**
A: The vulnerability IS that regular users can do admin things. Try anyway!

---

## 🏆 Good luck!

The automated tool should get you the flag in under 5 minutes. If something doesn't work, run the decoder to see what's actually in the SAML response, then adjust your approach.

Remember: This is about **configuration vulnerabilities**, not cryptographic attacks. The signature is valid - we're just exploiting who controls the signed content!

---

**Author**: GitHub Copilot  
**Challenge Author**: Bawolff  
**CTF**: InfobahnCTF  
**Date**: November 2025
