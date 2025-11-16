digits = [
    1,
    3,
    2,
    4,
    5,
    3,
    6,
    0,
    9,
    7,
    6,
    5,
    1,
    2,
    8,
    5,
    3,
    4,
    8,
    8,
    8,
    9,
    8,
    7,
    7,
    3,
    2,
    3,
    8,
    9,
    9,
    8,
    0,
    7,
    5,
    3,
    6,
    9,
    8,
    8,
    1,
    6,
    16,
    3,
    6,
    6,
    6,
]

print("All digits:", digits)
print()

# Two-digit ASCII codes
print("Two-digit ASCII interpretation:")
flag_chars = []
i = 0
while i < len(digits) - 1:
    # Try to form a two-digit ASCII code
    first = digits[i]
    second = digits[i + 1]

    # Handle 16 as special case (might be from 'a' = 10 + 6)
    if first == 16:
        val = first + 48  # Try as single digit with offset
        if 32 <= val < 128:
            flag_chars.append(chr(val))
        i += 1
        continue

    # Standard two-digit ASCII
    val = first * 10 + second
    print(f"  digits[{i}:{i+2}] = {first}{second} = {val} = ", end="")

    if 32 <= val < 128:
        char = chr(val)
        print(f"'{char}'")
        flag_chars.append(char)
        i += 2
    else:
        print(f"(out of range)")
        i += 1

flag = "".join(flag_chars)
print(f"\nDecoded flag: {flag}")
print(f"Wrapped: infobahn{{{flag}}}")
