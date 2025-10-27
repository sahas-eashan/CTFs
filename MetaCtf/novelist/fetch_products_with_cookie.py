import http.client, urllib.parse, re

BASE = "http://noneshallpass.chals.mctf.io"
parsed = urllib.parse.urlparse(BASE)
conn = http.client.HTTPConnection(parsed.netloc, timeout=10)
body = urllib.parse.urlencode({"username": "exploit_user", "password": "Expl0it!"})
headers = {"Content-Type": "application/x-www-form-urlencoded"}
conn.request("POST", "/login", body, headers)
res = conn.getresponse()
setcookie = res.getheader("Set-Cookie")
print("Set-Cookie:", setcookie)
res.read()
conn.close()
if not setcookie:
    print("no cookie")
    raise SystemExit
m = re.search(r"session=([^;]+)", setcookie)
if not m:
    print("no session")
    raise SystemExit
token = m.group(1)
print("token len", len(token))
# now fetch /products with cookie
conn = http.client.HTTPConnection(parsed.netloc, timeout=10)
req_headers = {"Cookie": "session=" + token}
conn.request("GET", "/products", headers=req_headers)
res = conn.getresponse()
html = res.read()
open("products_dump.html", "wb").write(html)
print("wrote products_dump.html, len", len(html))
conn.close()
