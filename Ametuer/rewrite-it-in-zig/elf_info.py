import struct

with open('chal','rb') as f:
    data = f.read()

EI_MAG = data[:4]
if EI_MAG != b'\x7fELF':
    raise SystemExit('not elf')

is_64 = data[4] == 2
if not is_64:
    raise SystemExit('not 64-bit')

endian = '<' if data[5] == 1 else '>'

# Elf64_Ehdr format
ELF_HDR_FMT = endian + 'HHIQQQIHHHHHH'
# start at offset 0x10
hdr = struct.unpack(ELF_HDR_FMT, data[0x10:0x10+struct.calcsize(ELF_HDR_FMT)])
(
    e_type,
    e_machine,
    e_version,
    e_entry,
    e_phoff,
    e_shoff,
    e_flags,
    e_ehsize,
    e_phentsize,
    e_phnum,
    e_shentsize,
    e_shnum,
    e_shstrndx,
) = hdr

print(f"e_type={e_type}, e_machine={hex(e_machine)}, entry=0x{e_entry:x}")
print(f"phoff=0x{e_phoff:x}, phnum={e_phnum}, phentsize={e_phentsize}")
print(f"shoff=0x{e_shoff:x}, shnum={e_shnum}, shentsize={e_shentsize}, shstrndx={e_shstrndx}")

PH_FMT = endian + 'IIQQQQQQ'
for i in range(e_phnum):
    off = e_phoff + i * e_phentsize
    pt, p_flags, p_offset, p_vaddr, p_paddr, p_filesz, p_memsz, p_align = struct.unpack(
        PH_FMT, data[off:off + struct.calcsize(PH_FMT)]
    )
    print(f"PH[{i}] type=0x{pt:x} flags=0x{p_flags:x} offset=0x{p_offset:x} vaddr=0x{p_vaddr:x} filesz=0x{p_filesz:x} memsz=0x{p_memsz:x} align=0x{p_align:x}")
