import base91
import bz2, lzma, zlib
import sys

# Read flag1.txt and decode base91
with open('flag1.txt', 'r', encoding='utf-8') as f:
    data = f.read().strip()

try:
    decoded = base91.decode(data)
    with open('flag2.bin', 'wb') as out:
        out.write(decoded)
    print('Saved base91-decoded output to flag2.bin')
except Exception as e:
    print('Base91 decode failed:', e)
    sys.exit(1)

# Try decompressing with common algorithms
for name, decompress in [
    ('bz2', bz2.decompress),
    ('lzma', lzma.decompress),
    ('zlib', zlib.decompress)
]:
    try:
        result = decompress(decoded)
        with open(f'flag2_{name}.bin', 'wb') as out:
            out.write(result)
        print(f'Decompressed with {name}, saved to flag2_{name}.bin')
    except Exception:
        pass

# Search for file signatures
signatures = {
    'ZIP': b'PK',
    'JPEG': b'\xff\xd8',
    'PNG': b'\x89PNG',
    'PDF': b'%PDF',
}
for name, sig in signatures.items():
    if sig in decoded:
        print(f'Found {name} signature in flag2.bin!')
