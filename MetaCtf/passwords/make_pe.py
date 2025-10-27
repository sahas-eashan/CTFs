import sys
with open('payload.bin','rb') as f:
    data=f.read()
idx = data.find(b'MZ')
if idx != -1:
    with open('payload_pe.bin','wb') as o:
        o.write(data[idx:])
