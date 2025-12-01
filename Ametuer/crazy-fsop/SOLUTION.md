# Crazy FSOP Solution

## Vulnerability Analysis

The challenge has several critical vulnerabilities:

1. **No bounds checking on index** - Can use negative or large indices
2. **No size validation** - Can allocate arbitrary sizes
3. **Use-after-free** - Can view freed chunks
4. **Double-free** - Can free same note multiple times

## Key Discoveries

### Memory Layout
```
.got:   0x3f78 - 0x4000
.data:  0x4000 - 0x4010
.bss:   0x4020 - 0x40c0
notes:  0x4040 (in BSS)
```

### GOT Access via Negative Indices
```
notes[-22] = free@got    (0x3f90)
notes[-21] = puts@got    (0x3f98)
notes[-18] = printf@got  (0x3fb0)
notes[-14] = malloc@got  (0x3fd0)
```

## Exploit Strategy

For glibc 2.42, we use House of Apple 2 / House of Emma FSOP technique:

1. **Leak libc** - Free large chunk into unsorted bin, leak fd pointer
2. **Leak heap** - Use tcache to leak heap address
3. **Create fake FILE structure** - Craft structure to redirect execution to system
4. **Tcache poisoning** - Use UAF to corrupt tcache bins
5. **Overwrite _IO_list_all** - Point to our fake FILE
6. **Trigger exit()** - Calls _IO_flush_all_lockp which processes our fake FILE

## Important Addresses (glibc 2.42)

```python
_IO_list_all = libc.base + 0x2354c0
_IO_2_1_stderr_ = libc.base + 0x2354e0
_IO_wfile_jumps = libc.base + 0x233228
system = libc.base + 0x5c4c0
```

## House of Apple 2 Requirements

The fake FILE structure must:
- Have `_flags` set appropriately
- Have `_wide_data` pointing to controlled memory
- Have `vtable` pointing to `_IO_wfile_jumps`
- Satisfy checks in `_IO_validate_vtable`

When `_IO_wfile_overflow` is called, it will:
1. Check `_wide_data->_IO_write_ptr > _wide_data->_IO_write_base`
2. Call `_wide_data->vtable->__doallocate`

We can make `__doallocate` point to `system` and set `_IO_buf_base` to "/bin/sh".

## Running the Exploit

```bash
# Install pwntools in WSL
pip3 install pwntools

# Run locally
python3 solve_final.py

# Run against remote
python3 solve_final.py REMOTE
```

## Notes

The challenge is named "Crazy FSOP" which strongly suggests FSOP is the intended solution, though other approaches may work depending on exact glibc version and protections.

For glibc 2.34+, traditional hooks (__free_hook, __malloc_hook) are removed, making FSOP one of the main exploitation techniques available.
