import requests
BASE_URL = "https://admin-panel-489a10b9570c.instancer.sekai.team"
sess = requests.Session()
resp = sess.get(f"{BASE_URL}/login.php", allow_redirects=False)
print(resp.status_code)
print(resp.headers.get("Set-Cookie"))
print(sess.cookies.get_dict())
