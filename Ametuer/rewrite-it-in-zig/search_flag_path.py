with open('chal','rb') as f:
    data=f.read()
for s in [b'/srv/app/flag', b'/app/flag', b'flag', b'/flag', b'/srv/app/run']:
    idx = data.find(s)
    if idx != -1:
        print(s, hex(idx))
