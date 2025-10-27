import requests

BASE_URL = "https://admin-panel-489a10b9570c.instancer.sekai.team"

data = {
    "username[]": "peppy",
    "password": "peppy",
}

r = requests.post(f"{BASE_URL}/login.php", data=data)
print(r.status_code)
print(r.text[:300])
