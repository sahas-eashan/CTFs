import pathlib

# Read chall.txt and manually decode the arithmetic sequences
code = pathlib.Path("chall.txt").read_text()

# Lines 7-11 contain long arithmetic sequences like:
# >~01+a*3+a*2+a*4+a*5+a*3+a*6+a*0+a*9+a*7+a*6v
# These are building numbers on the stack

# a = 10 in hex
# Each sequence: start with 0, add 1, then multiply by 10 and add digits


def decode_line(line: str) -> list[int]:
    """Decode a line like '01+a*3+a*2+a*4+' into the numbers it produces."""
    nums = []
    parts = (
        line.replace("v", "")
        .replace(">", "")
        .replace("<", "")
        .replace("~", "")
        .replace("^", "")
        .replace("*", "")
    )

    # Manual parsing - each pattern is: digit + (a * next_digit +)*
    # This builds: d0, d0*10+d1, (d0*10+d1)*10+d2, etc.
    # But we want the ADDITIONS, which give us digits

    # Simpler: just extract the digits after 'a*' or after '+'
    i = 0
    current = 0
    while i < len(parts):
        if parts[i : i + 2] == "01":
            current = 1
            i += 2
        elif parts[i] == "+":
            i += 1
        elif parts[i : i + 2] == "a":
            i += 1  # skip 'a'
        elif parts[i].isdigit() or parts[i] in "abcdef":
            digit = int(parts[i], 16)
            nums.append(digit)
            current = current * 10 + digit
            i += 1
        else:
            i += 1

    return nums


# Let's manually trace lines 7-11
lines = code.split("\n")

# Line 7: >~01+a*3+a*2+a*4+a*5+a*3+a*6+a*0+a*9+a*7+a*6v
# Line 8: v*a+8*a+8*a+8*a+4*a+3*a+5*a+8*a+2*a+1*a+5*a+<
# Line 9: >9+a*8+a*7+a*7+a*3+a*2+a*3+a*8+a*9+a*9+a*8+*v
# Line 10: v+0*a+7*a+5*a+3*a+6*a+9*a+8*a+8*a+1*a+6*a+10<
# Line 11: >a*3+a*6+a*6+a*6++>

print("Analyzing arithmetic sequences in chall.txt:")
print()

for i, line in enumerate(lines[7:12], start=7):
    print(f"Line {i}: {line}")

    # Extract just the digit sequences
    import re

    # Pattern: look for sequences like "a*DIGIT+" or just "DIGIT+"
    matches = re.findall(r"(?:a\*)?([0-9a-f])\+", line.lower())
    if matches:
        digits = [int(d, 16) for d in matches]
        print(f"  Digits: {digits}")
        # Try to interpret as ASCII
        ascii_try = "".join(
            chr(d + ord("0")) if d < 10 else chr(d - 10 + ord("a")) for d in digits
        )
        print(f"  As chars: {ascii_try}")
        # Or as raw values
        if all(32 <= d < 127 for d in digits):
            raw = "".join(chr(d) for d in digits)
            print(f"  As ASCII: {raw}")
    print()

# The pattern is: each number is built by multiplying by 10 and adding next digit
# So we need to extract what final numbers are being built
print("\nDecoding as decimal number sequences:")
for i, line in enumerate(lines[7:12], start=7):
    # Find all digit patterns
    cleaned = (
        line.replace("v", "")
        .replace(">", "")
        .replace("<", "")
        .replace("~", "")
        .replace("^", "")
        .replace("*", "")
    )

    # Extract digits in order
    digits = []
    for char in cleaned:
        if char in "0123456789":
            digits.append(int(char))
        elif char in "abcdef":
            digits.append(int(char, 16))

    print(f"Line {i} digits: {digits}")

    # Build numbers: 01+a*3+a*2+ means: 1, 1*10+3=13, 13*10+2=132
    # But for ASCII we want each digit interpreted differently
    # Let's try: maybe it's just the sequence of additions?

    # Actually looking at the pattern: the digits after + are the values we want
    # Let's extract them properly
    parts = re.split(r"[+*av<>~^]", line.lower())
    nums = [p for p in parts if p and p.isdigit()]
    print(f"  Number strings: {nums}")

    # Try ASCII interpretation
    try:
        ascii_chars = "".join(chr(int(n)) for n in nums if 32 <= int(n) < 127)
        if ascii_chars:
            print(f"  ASCII: {ascii_chars}")
    except:
        pass
    print()
