digits_str = "132453609765128534888987732389980753698816"

# Try all possible 2-digit interpretations with wraparound
print("2-digit ASCII with wraparound for low values:\n")

flag_chars = []
i = 0
while i < len(digits_str) - 1:
    pair = digits_str[i : i + 2]
    val = int(pair)

    if 32 <= val < 128:
        char = chr(val)
        print(f"  [{i:02d}] {pair} = {val} = '{char}'")
        flag_chars.append(char)
        i += 2
    elif val < 32:
        # Maybe add offset?
        ascii_with_offset = val + 48  # ASCII '0' = 48
        if 32 <= ascii_with_offset < 128:
            char = chr(ascii_with_offset)
            print(f"  [{i:02d}] {pair} = {val} + 48 = {ascii_with_offset} = '{char}'")
            flag_chars.append(char)
            i += 2
        else:
            i += 1
    else:
        i += 1

flag = "".join(flag_chars)
print(f"\nForward: {flag}")
print(f"Reversed: {flag[::-1]}")
print(f"\nWrapped forward: infobahn{{{flag}}}")
print(f"Wrapped reversed: infobahn{{{flag[::-1]}}}")

# Also try starting from different offsets
print("\n" + "=" * 50)
print("Trying offset by 1:")
flag_chars2 = []
i = 1
while i < len(digits_str) - 1:
    pair = digits_str[i : i + 2]
    val = int(pair)

    if 32 <= val < 128:
        char = chr(val)
        print(f"  [{i:02d}] {pair} = {val} = '{char}'")
        flag_chars2.append(char)
        i += 2
    elif val < 32:
        ascii_with_offset = val + 48
        if 32 <= ascii_with_offset < 128:
            char = chr(ascii_with_offset)
            print(f"  [{i:02d}] {pair} = {val} + 48 = {ascii_with_offset} = '{char}'")
            flag_chars2.append(char)
            i += 2
        else:
            i += 1
    else:
        i += 1

flag2 = "".join(flag_chars2)
print(f"\nForward: {flag2}")
print(f"Reversed: {flag2[::-1]}")
