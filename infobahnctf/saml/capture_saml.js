#!/usr/bin/env node
/**
 * Manual SAML Response Interceptor
 * Instructions for capturing SAML responses
 */

console.log('🔍 SAML Response Capture Guide\n');
console.log('Since automatic login is happening, we need to capture the SAML response manually.\n');

console.log('METHOD 1: Browser Network Tab');
console.log('================================');
console.log('1. Open DevTools (F12) → Network tab');
console.log('2. Clear all requests (trash icon)');
console.log('3. Visit: https://saml-web.challs.infobahnc.tf/flag');
console.log('4. You\'ll be redirected and see "not authorized" message');
console.log('5. In Network tab, find the request to /flag with query parameters');
console.log('6. Look for SAMLResponse parameter in the URL');
console.log('7. Copy the entire SAMLResponse value (will be long base64 string)');
console.log('8. Run: node saml_decoder.js "PASTE_SAMLRESPONSE_HERE"\n');

console.log('METHOD 2: Burp Suite / Proxy');
console.log('================================');
console.log('1. Configure browser to use Burp proxy');
console.log('2. Visit /flag endpoint');
console.log('3. Intercept the redirect from IdP back to SP');
console.log('4. Copy SAMLResponse parameter');
console.log('5. Decode it to see current username\n');

console.log('METHOD 3: Browser Console');
console.log('================================');
console.log('1. Visit: https://saml-web.challs.infobahnc.tf/flag');
console.log('2. Open Console (F12)');
console.log('3. Paste this code:');
console.log('   const params = new URLSearchParams(window.location.search);');
console.log('   console.log(params.get("SAMLResponse"));\n');

console.log('WHAT TO LOOK FOR:');
console.log('================================');
console.log('- Current username in SAML (should be "sahas")');
console.log('- Signature details');
console.log('- Property mapping being used');
console.log('- Any way to modify the username\n');

console.log('💡 ALTERNATIVE APPROACH:');
console.log('================================');
console.log('If we can\'t modify the IdP mappings via API (which seems to be the case),');
console.log('we need to look for other vulnerabilities:');
console.log('1. XML Signature Wrapping');
console.log('2. Comment injection in username');
console.log('3. SAML Response manipulation');
console.log('4. Race conditions');
console.log('5. Session fixation\n');
