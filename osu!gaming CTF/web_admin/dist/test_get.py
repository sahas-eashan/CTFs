import requests
BASE_URL = "https://admin-panel-489a10b9570c.instancer.sekai.team"
r = requests.get(f"{BASE_URL}/index.php")
print(r.status_code)
print(len(r.text))
