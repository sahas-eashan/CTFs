import bz2, lzma, zlib
import sys

# Read base91-decoded binary
with open("flag2.bin", "rb") as f:
    data = f.read()

# Try decompressing with common algorithms
for name, decompress in [
    ("bz2", bz2.decompress),
    ("lzma", lzma.decompress),
    ("zlib", zlib.decompress),
]:
    try:
        result = decompress(data)
        with open(f"flag3_{name}.bin", "wb") as out:
            out.write(result)
        print(f"Decompressed with {name}, saved to flag3_{name}.bin")
    except Exception:
        print(f"{name} decompression failed.")

# Try brute-force XOR
for key in range(256):
    xored = bytes(b ^ key for b in data)
    if b"CTF{" in xored or b"flag{" in xored or b"FLAG{" in xored:
        print(f"[XOR key {key}]", xored)
        with open(f"flag3_xor_{key}.bin", "wb") as out:
            out.write(xored)

# Search for file signatures
signatures = {
    "ZIP": b"PK",
    "JPEG": b"\xff\xd8",
    "PNG": b"\x89PNG",
    "PDF": b"%PDF",
}
for name, sig in signatures.items():
    if sig in data:
        print(f"Found {name} signature in flag2.bin!")
