# Try different offsets
sequences = [
    [0, 1, 3, 2, 4, 5, 3, 6, 0, 9, 7, 6],
    [5, 1, 2, 8, 5, 3, 4, 8, 8, 8, 9, 8],
    [9, 8, 7, 7, 3, 2, 3, 8, 9, 9, 8],
    [10, 6, 1, 8, 8, 9, 6, 3, 5, 7, 0],
]

for offset in [48, 64, 65, 87, 97]:
    print(f"\n{'='*60}")
    print(f"Offset: {offset} (adds to small values to make them letters/numbers)")
    print("=" * 60)

    all_chars = []
    for seq in sequences:
        for val in seq:
            char_val = val + offset
            if 32 <= char_val < 127:
                all_chars.append(chr(char_val))

    forward = "".join(all_chars)
    reversed_flag = forward[::-1]

    print(f"Forward:  {forward}")
    print(f"Reversed: {reversed_flag}")
    print(f"Wrapped:  infobahn{{{reversed_flag}}}")
