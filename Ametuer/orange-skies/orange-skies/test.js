import puppeteer from "puppeteer";
const payload = encodeURIComponent("fetch('/').then(()=>console.log('fetch ok')).catch(e=>console.log('fetch err',e.message))");
const url = `https://orange-skies-amateurs-ctf-2025.pages.dev/?xss=${payload}`;
const browser = await puppeteer.launch({headless:'new'});
const page = await browser.newPage();
page.on('console', msg => console.log('console:', msg.type(), msg.text()));
await page.goto(url, {waitUntil: 'load', timeout: 20000});
await page.waitForTimeout(3000);
await browser.close();
