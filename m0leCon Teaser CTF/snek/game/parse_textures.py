import struct

with open("snek", "rb") as f:
    data = f.read()

# texture_info located at offset ??? we need to find by symbol address 0x61e0 (virtual) - base 0x6000 (.data) -> offset 0x1e0 in .data
# .data section starts at file offset 0x5000 (from readelf). So file offset = 0x5000 + 0x1e0
DATA_OFFSET = 0x5000
TEXTURE_ADDR = 0x61e0
offset = DATA_OFFSET + (TEXTURE_ADDR - 0x6000)
entries = []
for i in range(22):
    entry = data[offset + i*0x30: offset + (i+1)*0x30]
    path = entry[:32].split(b"\x00",1)[0].decode()
    pixfmt, a, b, c = struct.unpack("<IIII", entry[32:])
    entries.append((path, pixfmt, a, b, c))

for idx, e in enumerate(entries):
    print(idx, e)
