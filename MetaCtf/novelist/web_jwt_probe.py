import urllib.request
import urllib.parse
import sys
import base64

BASE = "http://noneshallpass.chals.mctf.io"

opener = urllib.request.build_opener()


def post(path, params):
    url = BASE + path
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        resp = opener.open(req, timeout=10)
    except urllib.error.HTTPError as e:
        resp = e
    body = resp.read()
    headers = dict(resp.getheaders())
    return headers, body


def get(path):
    url = BASE + path
    req = urllib.request.Request(url)
    resp = opener.open(req, timeout=10)
    return dict(resp.getheaders()), resp.read()


def try_register_and_login():
    user = "exploit_user"
    pwd = "Expl0it!"
    print("[*] Registering user...")
    h, b = post("/register", {"username": user, "password": pwd, "confirm": pwd})
    print("Register headers:", h)
    print("Register body (preview):", b[:400])

    print("[*] Logging in...")
    h, b = post("/login", {"username": user, "password": pwd})
    print("Login headers:", h)
    print("Login body (preview):", b[:800])
    # check for Set-Cookie
    if "Set-Cookie" in h:
        print("Set-Cookie:", h["Set-Cookie"])
    # try to find token in body
    s = b.decode(errors="ignore")
    import re

    m = re.search(r"([A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)", s)
    if m:
        token = m.group(1)
        print("[+] Found JWT-like token in body:", token)
        analyze_jwt(token)
    else:
        print("No JWT-like token in body")

    # also check cookies via opener
    cj = opener.open(urllib.request.Request(BASE + "/products")).getheader("Set-Cookie")
    if cj:
        print("Products Set-Cookie:", cj)


def analyze_jwt(token):
    print("[*] decoding token...")
    parts = token.split(".")
    for i, p in enumerate(parts):
        pad = "=" * (-len(p) % 4)
        try:
            dec = base64.urlsafe_b64decode(p + pad)
            print(f"part {i}:", dec)
        except Exception as e:
            print("decode error", e)


if __name__ == "__main__":
    try:
        try_register_and_login()
    except Exception as e:
        print("Error:", e)
        sys.exit(1)
