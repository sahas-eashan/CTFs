#!/usr/bin/env python3
from pwn import *

context.arch = 'i386'

# Allowed: jmp, add, mov, sub, inc, dec, cmp, push, pop, int3
# The validation checks:
# 1. All instructions must contain one of the allowed mnemonics
# 2. JMP must be to an immediate address that's in the offsets list
# 3. Shellcode is prepended with: \xbc\x00\x70\x76\x06 (mov esp, 0x06767000)

# Key insight: The validation is on MNEMONIC strings, so:
# - "jmp" matches "jmp", "jmp short", "jmp near", etc.
# - We can use registers with these instructions
# - The JMP immediate check only applies if it's a JMP with immediate operand

# Strategy: Write shellcode to stack, then use jmp to register
# But wait - "jmp esp" would show as "jmp" mnemonic with register operand (not immediate)
# So it would pass the immediate check (because target.type != X86_OP_IMM)

# Let's create shellcode that:
# 1. Pushes actual shellcode (with int 0x80) to stack
# 2. Uses jmp esp or similar to execute it

# But actually, looking more carefully at the code:
# if target.type != X86_OP_IMM:
#     exit("jmp must be imm")
# So jmp MUST be immediate! We can't use jmp esp.

# Alternative approach: Use self-modifying code
# Write bytes to the code segment and then jump there with immediate address

# The shellcode is loaded at 0x1337000 (based on disasm address)
# We can write to memory and jump to a known offset

# Build shellcode that modifies itself:
sc = b""

# We'll write "int 0x80" (0xcd 0x80) to memory location after our setup code
# Then jump to a sequence that uses it

# Calculate addresses:
# Base address: 0x1337000 + 5 (for the initial mov esp)
base = 0x1337000 + 5

# Let's put the real shellcode at offset 0x100
target_offset = 0x100
target_addr = base + target_offset

# First, set up what we'll write
# We want to write a sequence like:
# int 0x80; <ret or jmp>

# Use mov to write bytes to memory
# mov byte [addr], imm

# Let's build it:
offset = 0

# Write "int 0x80" to memory at target location
# int 0x80 = 0xcd 0x80

# We need to use 32-bit mov instructions
# mov dword ptr [0x1337100], 0x??????cd80

# Actually, let's use a simpler technique:
# Use the stack! The stack is writable and we control esp

# New strategy:
# 1. Push a complete shellcode payload onto stack (including int 0x80)
# 2. Adjust esp to point to it
# 3. Use "jmp" to a calculated immediate address on stack

# But we can't know the exact stack address to jump to...

# Better idea: Use mov to write to a known location in our code segment
# The shellcode area is writable when being constructed

# Wait, actually the simplest approach:
# Since "add", "sub", "inc", "dec" are allowed, we can modify memory!
# We can ADD to a byte in our code to turn it into "int 0x80"

# Plan:
# 1. Have a placeholder (like 0xcd 0x00) in our code
# 2. Use add/inc to change 0x00 to 0x80
# 3. Jump to that location

# Let's implement this:

# Calculate offset for our "modified" code section
mod_offset = 100  # We'll put modifiable code here
mod_addr = base + mod_offset

# Build the exploit
payload = b""

# First, modify the byte at our target location
# We'll have "cd 00" (int 0) and change it to "cd 80" (int 0x80)

# To modify: mov byte ptr [addr], value; then add byte ptr [addr], delta
# But mov byte ptr might not be allowed in the same way...

# Simpler: Use the pattern where we have "cd 7f" and inc it to "cd 80"

# Let's put this after our initial setup:
# We'll jump past setup, then have the modified code, then the setup

# Actually, let's think differently:
# What if we use the stack pointer manipulation and push/pop?

# New approach: Abuse the allowed instructions more cleverly
# We can use "pop" to execute values from stack as code? No...

# Let me try yet another angle:
# Use integer underflow/overflow with add/sub to write values

# Simplest working approach:
# Just write shellcode that uses only the allowed instructions to do useful work
# Can we read a file using only: mov, add, sub, push, pop, inc, dec, jmp, cmp, int3?

# Wait! INT3 is allowed! That's a software breakpoint.
# But we need INT 0x80 for syscalls...

# Hmm, let me check if there's a way to use int3 creatively
# int3 = 0xcc, int 0x80 = 0xcd 0x80
# They're different instructions

# Final approach: Exploit the disassembler itself!
# What if we craft bytes that disassemble as allowed instructions
# but when executed do something else?

# Or use the fact that x86 has variable length instructions
# and we can hide forbidden instructions within "allowed" ones

print("Trying disassembler confusion technique...")

# Craft bytes that:
# - Disassemble as allowed instructions
# - But execute as different instructions due to alignment

# Example: Use multi-byte instructions where the tail bytes form other instructions

# Let's try this payload:
# We'll use the fact that some allowed instructions can have prefixes/suffixes

confused_sc = b""

# Try: Use instruction that disassembles as "jmp" but includes other bytes
# jmp with unnecessary prefixes?

# Or: Use overlapping instructions
# Place bytes such that:
# - If disassembled from offset 0: looks like allowed instructions
# - If executed from offset 1: contains int 0x80

# Create the payload
# Start with a jmp to skip over the "data"
confused_sc += asm(f"jmp {base + 20}")  # Jump to actual code

# At offset ~5-19: place bytes that contain "cd 80" (int 0x80)
# But make sure when disassembled they look innocent
confused_sc += b"\xcd\x80"  # int 0x80 - we'll hide this

# Continue...

# Actually, I realize the check is quite strict
# Let me read the validation more carefully:
# 1. It disassembles ALL bytes
# 2. Checks each instruction's mnemonic
# 3. Validates jumps
# 4. Ensures all bytes are decoded

# So we can't hide instructions - they'll all be disassembled

# The REAL trick: Look at what instructions are actually allowed
# "push" and "pop" are allowed!
# We can push addresses and "pop" into  eip? No, pop eip isn't valid

# Let me check: can we use "pop" with segment registers or special regs?

# Actually,wait - can we use MOV with segment registers to cause issues?

# Let me try a completely different approach:
# Use only the allowed instructions to build a proper payload

# Syscalls without int 0x80:
# - sysenter (0f 34)
# - syscall (0f 05)
# - Using VDSO
# These are also forbidden

# But wait - can we jump to existing code in libc or vdso?
# We'd need to know addresses (ASLR) and construct the jump

# Aha! What if the template.elf already contains useful code?
# Let me check what's in template.elf besides our shellcode

# For now, let me try a simpler shellcode to test:

test_payload = b""
test_payload += asm("mov eax, 1")  # exit syscall
test_payload += asm("mov ebx, 42")
# We need int 0x80 here but can't have it...

# This won't work without int 0x80

# Let me try to see if I can write directly to stdout using memory-mapped I/O
# or other techniques

# Or... what if we trigger a crash that reveals information?

# Let me just try pushing data and see what happens
crash_test = b""
crash_test += asm("push 0x41414141")
crash_test += asm("push 0x42424242")
crash_test += asm("int3")  # Break

print(crash_test.hex())

# For now, let me try to connect and see what happens

if args.LOCAL:
    p = process(['python3', 'chal.py'])
else:
    p = remote('amt.rs', 57207)

p.sendlineafter(b'shellcode: ', crash_test.hex().encode())
print(p.recvall(timeout=2))
