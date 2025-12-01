#!/usr/bin/env python3
from pwn import *

print("Connecting to check what server sends...")
io = remote('amt.rs', 57207)

print("Receiving initial data...")
data = io.recv(timeout=5)
print(f"Received ({len(data)} bytes):")
print(repr(data))
print(data.decode(errors='ignore'))

io.close()
