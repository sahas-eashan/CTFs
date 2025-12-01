import base64, bz2, lzma, zlib
import string

# Read flag1.txt
with open('flag1.txt', 'r', encoding='utf-8') as f:
    data = f.read().strip()

# Try decompressing with common algorithms
for name, decompress in [
    ('bz2', lambda d: bz2.decompress(d)),
    ('lzma', lambda d: lzma.decompress(d)),
    ('zlib', lambda d: zlib.decompress(d))
]:
    try:
        # Try as bytes
        result = decompress(data.encode())
        print(f'[{name}]', result)
    except Exception:
        pass
    try:
        # Try as ascii
        result = decompress(bytes(data, 'ascii'))
        print(f'[{name}-ascii]', result)
    except Exception:
        pass

# Try brute-force XOR
for key in range(256):
    xored = ''.join(chr(ord(c) ^ key) for c in data)
    if any(flag in xored for flag in ['CTF{', 'flag{', 'FLAG{']):
        print(f'[XOR key {key}]', xored)

# Try extracting printable substrings
printable = ''.join(c if c in string.printable else '.' for c in data)
print('[Printable]', printable)

# Try base91 decode (if you have a base91 lib, otherwise skip)
try:
    import base91
    decoded = base91.decode(data)
    print('[base91]', decoded)
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
    if sig in data.encode():
        print(f'Found {name} signature!')
