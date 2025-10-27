import base64, json, time, hmac, hashlib, sys
secret = sys.argv[1]
kid = sys.argv[2] if len(sys.argv) > 2 else None
header = {"alg":"HS256","typ":"JWT"}
if kid:
    header["kid"] = kid
payload = {"user_id":1,"username":"admin","balance":9999.0,"role":"admin","exp":int(time.time())+3600}

def b64(data):
    return base64.urlsafe_b64encode(json.dumps(data, separators=(',',':')).encode()).decode().rstrip('=')

def sign(msg, secret):
    return base64.urlsafe_b64encode(hmac.new(secret.encode(), msg.encode(), hashlib.sha256).digest()).decode().rstrip('=')

segments = [b64(header), b64(payload)]
msg = '.'.join(segments)
signature = sign(msg, secret)
print(f"{msg}.{signature}")
