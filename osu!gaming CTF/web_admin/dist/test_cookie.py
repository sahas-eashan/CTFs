import requests

BASE_URL = "https://admin-panel-489a10b9570c.instancer.sekai.team"
resp = requests.post(f"{BASE_URL}/login.php", data={'username':'peppy','password':'test'})
print(resp.status_code)
print(resp.headers.get('Set-Cookie'))
