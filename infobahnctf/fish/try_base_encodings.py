import base64

digits = "132453609765128534888987732389980753698816"

# Try hex interpretation (need even length - 42 digits, take first 40)
print("=== HEX Interpretation ===")
try:
    hex_str = digits[:40]  # 40 digits = 20 bytes
    bytes_data = bytes.fromhex(hex_str)
    print(f"Hex ({hex_str}): {bytes_data}")
    print(f"As ASCII: {bytes_data.decode('ascii', errors='ignore')}")
except Exception as e:
    print(f"Error: {e}")

# Maybe it's octal? Groups of 3
print("\n=== OCTAL Interpretation ===")
flag_chars = []
i = 0
while i < len(digits) - 2:
    triple = digits[i:i+3]
    val = int(triple, 8)  # Parse as octal
    if 32 <= val < 128:
        flag_chars.append(chr(val))
        print(f"{triple} (octal) = {val} = '{chr(val)}'")
    i += 3

if flag_chars:
    forward = ''.join(flag_chars)
    reversed_flag = forward[::-1]
    print(f"\nForward: {forward}")
    print(f"Reversed: {reversed_flag}")
    print(f"Wrapped: infobahn{{{reversed_flag}}}")
