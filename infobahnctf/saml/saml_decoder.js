#!/usr/bin/env node
/**
 * SAML Response Decoder
 * Decodes and pretty-prints SAML responses from base64+deflate format
 * 
 * Usage:
 *   node saml_decoder.js <base64_encoded_saml_response>
 *   node saml_decoder.js --from-url "https://example.com/flag?SAMLResponse=..."
 */

const zlib = require('zlib');
const { DOMParser, XMLSerializer } = require('xmldom');

// Color output helpers
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  red: '\x1b[31m',
  cyan: '\x1b[36m'
};

function colorize(text, color) {
  return `${colors[color]}${text}${colors.reset}`;
}

function decodeSAMLResponse(base64Response) {
  try {
    console.log(colorize('\n[+] Decoding SAML Response...', 'blue'));
    
    // Step 1: Base64 decode
    const compressed = Buffer.from(base64Response, 'base64');
    console.log(colorize(`[+] Base64 decoded: ${compressed.length} bytes`, 'green'));
    
    // Step 2: Inflate (decompress)
    const xmlString = zlib.inflateRawSync(compressed).toString('utf-8');
    console.log(colorize(`[+] Decompressed: ${xmlString.length} characters`, 'green'));
    
    // Step 3: Parse XML
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlString, 'application/xml');
    
    console.log(colorize('\n[+] XML Structure:', 'bright'));
    console.log(colorize('='.repeat(80), 'cyan'));
    
    // Pretty print with indentation
    const serializer = new XMLSerializer();
    const prettyXml = formatXml(xmlString);
    console.log(prettyXml);
    console.log(colorize('='.repeat(80), 'cyan'));
    
    // Extract key information
    console.log(colorize('\n[+] Extracted Information:', 'bright'));
    
    // Find root element ID
    const rootId = xmlDoc.documentElement.getAttribute('ID');
    console.log(colorize(`  Root ID: `, 'yellow') + rootId);
    
    // Find signature
    const signatures = xmlDoc.getElementsByTagName('Signature');
    if (signatures.length > 0) {
      console.log(colorize(`  Signatures found: ${signatures.length}`, 'yellow'));
      
      const sig = signatures[0];
      const references = sig.getElementsByTagName('Reference');
      if (references.length > 0) {
        const refUri = references[0].getAttribute('URI');
        console.log(colorize(`  Reference URI: `, 'yellow') + refUri);
        
        // List transforms
        const transforms = sig.getElementsByTagName('Transform');
        console.log(colorize(`  Transforms (${transforms.length}):`, 'yellow'));
        for (let i = 0; i < transforms.length; i++) {
          const algo = transforms[i].getAttribute('Algorithm');
          console.log(`    - ${algo}`);
        }
      }
      
      // Signature algorithm
      const sigMethod = sig.getElementsByTagName('SignatureMethod')[0];
      if (sigMethod) {
        console.log(colorize(`  Signature Algorithm: `, 'yellow') + sigMethod.getAttribute('Algorithm'));
      }
    }
    
    // Find username attribute
    const attributes = xmlDoc.getElementsByTagName('Attribute');
    console.log(colorize(`\n[+] SAML Attributes (${attributes.length}):`, 'bright'));
    
    for (let i = 0; i < attributes.length; i++) {
      const attr = attributes[i];
      const name = attr.getAttribute('Name');
      const values = attr.getElementsByTagName('AttributeValue');
      
      if (values.length > 0) {
        const value = values[0].textContent || values[0].text || '';
        
        // Highlight username attribute
        if (name.includes('username')) {
          console.log(colorize(`  ${name}:`, 'green') + colorize(` "${value}"`, 'bright'));
        } else {
          console.log(`  ${name}: "${value}"`);
        }
      }
    }
    
    // Security checks
    console.log(colorize('\n[+] Security Analysis:', 'bright'));
    
    const sigCount = signatures.length;
    if (sigCount === 0) {
      console.log(colorize('  ⚠️  WARNING: No signature found!', 'red'));
    } else if (sigCount > 1) {
      console.log(colorize(`  ⚠️  WARNING: Multiple signatures (${sigCount}) - potential wrapper attack!`, 'red'));
    } else {
      console.log(colorize('  ✓ Single signature detected', 'green'));
    }
    
    // Check for multiple username attributes
    let usernameCount = 0;
    for (let i = 0; i < attributes.length; i++) {
      if (attributes[i].getAttribute('Name').includes('username')) {
        usernameCount++;
      }
    }
    
    if (usernameCount > 1) {
      console.log(colorize(`  ⚠️  WARNING: Multiple username attributes (${usernameCount})!`, 'red'));
    }
    
    return xmlString;
    
  } catch (error) {
    console.error(colorize(`\n[!] Error: ${error.message}`, 'red'));
    console.error(colorize('[!] Make sure the input is a valid base64-encoded deflated SAML response', 'red'));
    throw error;
  }
}

function formatXml(xml) {
  const PADDING = '  ';
  const reg = /(>)(<)(\/*)/g;
  let pad = 0;
  
  xml = xml.replace(reg, '$1\n$2$3');
  
  return xml.split('\n').map((node) => {
    let indent = 0;
    if (node.match(/.+<\/\w[^>]*>$/)) {
      indent = 0;
    } else if (node.match(/^<\/\w/) && pad > 0) {
      pad -= 1;
    } else if (node.match(/^<\w[^>]*[^\/]>.*$/)) {
      indent = 1;
    } else {
      indent = 0;
    }
    
    const padding = PADDING.repeat(pad);
    pad += indent;
    
    return padding + node;
  }).join('\n');
}

function extractFromUrl(url) {
  const match = url.match(/[?&]SAMLResponse=([^&]+)/);
  if (!match) {
    throw new Error('No SAMLResponse parameter found in URL');
  }
  return decodeURIComponent(match[1]);
}

// Main execution
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    console.log(colorize('\nSAML Response Decoder', 'bright'));
    console.log('Usage:');
    console.log('  node saml_decoder.js <base64_encoded_response>');
    console.log('  node saml_decoder.js --from-url "https://example.com/flag?SAMLResponse=..."');
    console.log('\nExamples:');
    console.log('  node saml_decoder.js H4sIAAAAAAAA...');
    console.log('  node saml_decoder.js --from-url "$(pbpaste)"');
    process.exit(0);
  }
  
  let samlResponse;
  
  if (args[0] === '--from-url') {
    if (args.length < 2) {
      console.error(colorize('[!] Error: URL required after --from-url', 'red'));
      process.exit(1);
    }
    samlResponse = extractFromUrl(args[1]);
  } else {
    samlResponse = args[0];
  }
  
  try {
    decodeSAMLResponse(samlResponse);
    console.log(colorize('\n[+] Done!', 'green'));
  } catch (error) {
    process.exit(1);
  }
}

module.exports = { decodeSAMLResponse, extractFromUrl };
