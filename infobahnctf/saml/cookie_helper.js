#!/usr/bin/env node
/**
 * Cookie Extraction Helper
 * Helps format cookies from various sources for use with authentik_api.js
 */

const fs = require('fs');

console.log('🍪 Cookie Extraction Helper\n');
console.log('This tool helps format your Authentik session cookie.\n');

// Method 1: From browser DevTools
console.log('📋 METHOD 1: Browser DevTools (Recommended)');
console.log('   1. Login to https://saml-web.challs.infobahnc.tf');
console.log('   2. Press F12 to open DevTools');
console.log('   3. Go to: Application → Storage → Cookies');
console.log('   4. Find and copy the value of "authentik_session"');
console.log('   5. Use it like this:\n');
console.log('      node authentik_api.js --target https://saml-web.challs.infobahnc.tf \\');
console.log('        --session "authentik_session=YOUR_VALUE_HERE"\n');

// Method 2: From browser console
console.log('📋 METHOD 2: Browser Console (Quick)');
console.log('   1. Login to the site');
console.log('   2. Press F12 → Console tab');
console.log('   3. Paste this code and press Enter:\n');
console.log('      document.cookie\n');
console.log('   4. Copy the entire output');
console.log('   5. Use the full string with --session flag\n');

// Method 3: From Burp Suite
console.log('📋 METHOD 3: Burp Suite / HTTP Proxy');
console.log('   1. Capture any request to the Authentik server');
console.log('   2. Find the "Cookie:" header');
console.log('   3. Copy everything after "Cookie: "');
console.log('   4. Use it with --session flag\n');

// Method 4: From curl output
console.log('📋 METHOD 4: Extract from curl -v output');
console.log('   1. Make authenticated request with curl -v');
console.log('   2. Look for "< Set-Cookie: authentik_session=..."');
console.log('   3. Copy the cookie value\n');

// Interactive helper
const args = process.argv.slice(2);

if (args.length > 0) {
  const input = args.join(' ');
  
  console.log('🔍 Analyzing your input...\n');
  
  // Try to extract authentik_session
  const sessionMatch = input.match(/authentik_session=([^;\s]+)/);
  const csrfMatch = input.match(/csrftoken=([^;\s]+)/);
  
  if (sessionMatch) {
    console.log('✅ Found authentik_session cookie!\n');
    
    let formattedCookie = `authentik_session=${sessionMatch[1]}`;
    
    if (csrfMatch) {
      console.log('✅ Found csrftoken too!\n');
      formattedCookie += `; csrftoken=${csrfMatch[1]}`;
    }
    
    console.log('📋 Use this exact string:\n');
    console.log(`   "${formattedCookie}"\n`);
    
    console.log('📝 Full command:\n');
    console.log(`   node authentik_api.js --target https://saml-web.challs.infobahnc.tf --session "${formattedCookie}"\n`);
    
    // Optionally save to file
    fs.writeFileSync('cookie.txt', formattedCookie);
    console.log('💾 Also saved to cookie.txt for convenience!\n');
    
  } else {
    console.log('❌ Could not find authentik_session in your input.');
    console.log('   Make sure you copied the cookie value correctly.\n');
    console.log('   Expected format: authentik_session=xyz123...\n');
  }
} else {
  console.log('💡 TIP: You can also pass cookie string as argument:\n');
  console.log('   node cookie_helper.js "authentik_session=xyz123..."\n');
  console.log('   This will format it correctly for you!\n');
}

// Test cookie validity helper
console.log('🧪 To test if your cookie works:\n');
console.log('   1. Windows PowerShell:\n');
console.log('      $headers = @{ "Cookie" = "YOUR_COOKIE_HERE" }');
console.log('      Invoke-RestMethod -Uri "https://saml-web.challs.infobahnc.tf/api/v3/core/users/me/" -Headers $headers\n');
console.log('   2. Linux/Mac (curl):\n');
console.log('      curl -b "YOUR_COOKIE_HERE" https://saml-web.challs.infobahnc.tf/api/v3/core/users/me/\n');
console.log('   If you see your user info → Cookie is valid! ✅\n');
