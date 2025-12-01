from PIL import Image
import numpy as np
import base64
import base91

FLAG_PREFIXES = [b"amateursCTF{", b"CTF{"]


def is_mostly_printable(b, min_run=20):
    run = 0
    for ch in b:
        if 32 <= ch <= 126:
            run += 1
            if run >= min_run:
                return True
        else:
            run = 0
    return False


def scan_for_flags(label, data):
    print(f"[+] Scanning {label}, {len(data)} bytes")
    # direct flag
    for pref in FLAG_PREFIXES:
        if pref in data:
            start = data.index(pref)
            # naive brace close
            if b"}" in data[start : start + 128]:
                end = data.index(b"}", start) + 1
                print(f"    >>> POSSIBLE FLAG ({label}): {data[start:end]!r}")
    # printable runs
    if is_mostly_printable(data):
        text = data.decode("ascii", errors="ignore")
        print(f"    [printable] sample: {text[:200]!r}")

    # quick header hints
    if data.startswith(b"\x1f\x8b"):
        print("    [hint] gzip header found")
    if b"BZh" in data[:200]:
        print("    [hint] Bzip header near start")
    if data.startswith(b"PK\x03\x04"):
        print("    [hint] zip header found")


def main():
    img = Image.open("output.png")
    pixels = np.array(img)
    red = pixels[:, :, 0]

    # foreground mask: red != 7
    mask = (red != 7).astype(np.uint8).flatten()
    red_vals = red.flatten()

    # 1 bit per pixel (presence of foreground)
    bits1 = mask
    # pack into bytes, MSB-first
    bytes1 = bytearray()
    for i in range(0, len(bits1) - 7, 8):
        b = 0
        for j in range(8):
            b = (b << 1) | bits1[i + j]
        bytes1.append(b)
    scan_for_flags("1bit_mask", bytes(bytes1))

    # 1 bit per pixel, but only where red != 7, derive bit from parity of red
    fg_positions = np.where(red_vals != 7)[0]
    bits_parity = ((red_vals[fg_positions] & 1)).astype(np.uint8)
    bytes_parity = bytearray()
    for i in range(0, len(bits_parity) - 7, 8):
        b = 0
        for j in range(8):
            b = (b << 1) | bits_parity[i + j]
        bytes_parity.append(b)
    scan_for_flags("1bit_parity_foreground", bytes(bytes_parity))

    # try (red-7) & 3 as 2 bits/pixel, foreground only
    two_bits = ((red_vals[fg_positions] - 7) & 3).astype(np.uint8)
    bits2 = []
    for v in two_bits:
        bits2.append((v >> 1) & 1)
        bits2.append(v & 1)
    bytes2 = bytearray()
    for i in range(0, len(bits2) - 7, 8):
        b = 0
        for j in range(8):
            b = (b << 1) | bits2[i + j]
        bytes2.append(b)
    data2 = bytes(bytes2)
    scan_for_flags("2bit_red_offset", data2)

    # if any stream looks printable, also try base64/base91
    for label, data in [
        ("1bit_mask", bytes(bytes1)),
        ("1bit_parity_foreground", bytes(bytes_parity)),
        ("2bit_red_offset", data2),
    ]:
        ascii_view = data.decode("ascii", errors="ignore")
        if any(c.isalnum() for c in ascii_view):
            # Base64 attempt
            cleaned = "".join(
                c
                for c in ascii_view
                if c
                in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
            )
            if len(cleaned) > 0 and len(cleaned) % 4 == 0:
                try:
                    b64_dec = base64.b64decode(cleaned, validate=False)
                    scan_for_flags(label + "_b64", b64_dec)
                except Exception:
                    pass
            # Base91 attempt
            try:
                b91_dec = base91.decode(ascii_view)
                scan_for_flags(label + "_b91", b91_dec)
            except Exception:
                pass


if __name__ == "__main__":
    main()
