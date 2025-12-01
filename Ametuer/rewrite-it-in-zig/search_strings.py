with open('chal','rb') as f:
    data=f.read()
for s in [b'/bin/sh', b'/bin/bash', b'sh\x00']:
    idx = data.find(s)
    if idx != -1:
        print(s, hex(idx))
