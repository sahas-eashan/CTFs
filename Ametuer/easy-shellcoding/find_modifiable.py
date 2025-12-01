#!/usr/bin/env python3
from capstone import *

# We need to find bytes that:
# 1. Disassemble as an allowed instruction
# 2. Can be modified by adding/subbing a value to become "cd 80" (int 0x80)

ALLOWED = ["jmp", "add", "mov", "sub", "inc", "dec", "cmp", "push", "pop", "int3"]

target = b"\xcd\x80"  # int 0x80

# Try different byte patterns
cs = Cs(CS_ARCH_X86, CS_MODE_32)
cs.detail = True

print("Looking for modifiable patterns...")
print("=" * 60)

# Idea 1: Find instruction that starts with 0xcd
# Then we can modify the second byte

for second_byte in range(256):
    if second_byte == 0x80:
        continue  # Skip the target

    test_bytes = bytes([0xcd, second_byte])
    try:
        insns = list(cs.disasm(test_bytes, 0x1000))
        if len(insns) > 0:
            insn = insns[0]
            if any(part in insn.mnemonic for part in ALLOWED):
                diff = 0x80 - second_byte
                if -128 <= diff <= 127:  # Can be done with add byte
                    print(f"Found: {test_bytes.hex()} = {insn.mnemonic} {insn.op_str}")
                    print(f"  -> Need to add {diff} (0x{diff & 0xff:02x}) to second byte")
                    print()
    except:
        pass

# Idea 2: Find 2-byte sequence that can be modified byte-by-byte
print("\n" + "=" * 60)
print("Alternate idea: Use a different instruction and modify multiple bytes")
print("=" * 60)

# What if we use:
# - "cmp al, 0xXX" (0x3c XX) and modify both bytes?
# - "mov al, XX" (0xb0 XX) and modify both bytes?
# - "push XX" (0x6a XX for single byte) and modify?

# Let's try "cmp al, X" -> modify to "int 0x80"
# 3c XX -> cd 80
# First byte: 3c + delta1 = cd => delta1 = 0x91
# Second byte: XX + delta2 = 80

test = b"\x3c\x00"
insns = list(cs.disasm(test, 0x1000))
if insns:
    print(f"{test.hex()}: {insns[0].mnemonic} {insns[0].op_str}")
    print(f"  Need to add 0x91 to first byte, 0x80 to second")
    print(f"  Total: 2 modifications")
    print()

# Or use "dec esp" (0x4c) as a starting byte?
# No, 0x4c is "dec esp" in 32-bit

# Better: Look for a NOP-like sequence we can modify
# "inc eax" = 0x40
# "inc ecx" = 0x41
# etc.

# What about using "add" instruction itself as the target?
# "add al, 0xXX" = 0x04 XX

test = b"\x04\x00"
insns = list(cs.disasm(test, 0x1000))
if insns:
    print(f"{test.hex()}: {insns[0].mnemonic} {insns[0].op_str}")
    delta1 = 0xcd - 0x04
    delta2 = 0x80 - 0x00
    print(f"  Need to add 0x{delta1:02x} to first byte, 0x{delta2:02x} to second")
    print()

# Try "sub al, XX"
test = b"\x2c\x00"
insns = list(cs.disasm(test, 0x1000))
if insns:
    print(f"{test.hex()}: {insns[0].mnemonic} {insns[0].op_str}")
    delta1 = 0xcd - 0x2c
    delta2 = 0x80 - 0x00
    print(f"  Need to add 0x{delta1:02x} to first byte, 0x{delta2:02x} to second")
    print()

# Most practical: Use "int3" (0xcc) and modify next byte!
# cc XX -> cc (int3) then next instruction
# But we want cd 80

print("=" * 60)
print("BEST OPTION: Use two separate bytes")
print("=" * 60)

# Put "inc eax" (0x40) followed by "dec eax" (0x48)
# Then modify: 0x40 -> 0xcd (add 0x8d), 0x48 -> 0x80 (sub 0xc8 or add 0x38)

test = b"\x40\x48"
insns = list(cs.disasm(test, 0x1000))
for insn in insns:
    print(f"{insn.bytes.hex()}: {insn.mnemonic} {insn.op_str}")

print("\nModifications needed:")
print(f"  Byte 1: 0x40 + 0x8d = 0xcd")
print(f"  Byte 2: 0x48 - 0xc8 = 0x80 (or 0x48 + 0x38 = 0x80)")
print()

# Test another combo
test = b"\x40\x40"  # inc eax, inc eax
insns = list(cs.disasm(test, 0x1000))
for insn in insns:
    print(f"{insn.bytes.hex()}: {insn.mnemonic} {insn.op_str}")

delta1 = 0xcd - 0x40
delta2 = 0x80 - 0x40
print(f"\n  Byte 1: 0x40 + 0x{delta1:02x} = 0xcd")
print(f"  Byte 2: 0x40 + 0x{delta2:02x} = 0x80")
