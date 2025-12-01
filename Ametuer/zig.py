import struct
import sys

def analyze_binary(path):
    try:
        with open(path, 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find '{path}'. Make sure it is in the current folder.")
        return

    print(f"[*] Analyzing {path} ({len(data)} bytes)...")

    # 1. Parse ELF Header (64-bit)
    # e_entry is at offset 0x18 (8 bytes)
    e_entry = struct.unpack('<Q', data[0x18:0x20])[0]
    # e_phoff (Program Header Offset) is at 0x20 (8 bytes)
    e_phoff = struct.unpack('<Q', data[0x20:0x28])[0]
    # e_phnum (Number of Program Headers) is at 0x38 (2 bytes)
    e_phnum = struct.unpack('<H', data[0x38:0x3A])[0]
    
    print(f"[*] Entry Point: {hex(e_entry)}")
    
    # 2. Check Stack Executability (GNU_STACK)
    is_stack_exec = False
    load_base = 0x400000 # Standard for 64-bit static
    
    # Iterate Program Headers
    for i in range(e_phnum):
        offset = e_phoff + (i * 56) # 56 bytes per PHdr
        p_type = struct.unpack('<I', data[offset:offset+4])[0]
        p_flags = struct.unpack('<I', data[offset+4:offset+8])[0]
        
        # PT_GNU_STACK = 0x6474e551
        if p_type == 0x6474e551:
            if p_flags & 0x1: # PF_X
                is_stack_exec = True
                print("[!] STACK IS EXECUTABLE (RWX). Shellcode strategy recommended.")
            else:
                print("[*] Stack is NX (Not Executable). ROP strategy required.")
    
    # 3. Gadget Scanner
    # We search raw bytes for opcodes. 
    # Since it is static, the file offset roughly maps to Virtual Address = Base + Offset
    # NOTE: This assumes standard loading. If PIE is on, this might vary, but 'file' said static.
    
    # Gadgets to find:
    # pop rdi; ret = 5f c3
    # pop rax; ret = 58 c3
    # pop rsi; ret = 5e c3
    # pop rdx; ret = 5a c3
    # syscall      = 0f 05
    
    gadgets = {
        "pop rdi; ret": b'\x5f\xc3',
        "pop rax; ret": b'\x58\xc3',
        "pop rsi; ret": b'\x5e\xc3',
        "pop rdx; ret": b'\x5a\xc3',
        "syscall":      b'\x0f\x05'
    }
    
    results = {}
    
    print("\n[*] Scanning for Gadgets...")
    for name, byte_seq in gadgets.items():
        offset = data.find(byte_seq)
        if offset != -1:
            # Approximate VA: Usually Offset + 0x400000 for static binaries
            # However, we should check the LOAD segment to be precise.
            # For now, we use the raw offset + 0x400000 as a good guess for static binaries.
            va = 0x400000 + offset 
            results[name] = va
            print(f"    Found '{name}' at offset {hex(offset)} -> VA {hex(va)}")
        else:
            print(f"    Failed to find '{name}'")

    print("\n[*] Check for '/bin/sh' string...")
    binsh = data.find(b'/bin/sh')
    if binsh != -1:
        binsh_va = 0x400000 + binsh
        print(f"    Found '/bin/sh' at {hex(binsh_va)}")
        results['binsh'] = binsh_va
    else:
        print("    '/bin/sh' not found.")

    return is_stack_exec, results

if __name__ == "__main__":
    analyze_binary("./chal")
