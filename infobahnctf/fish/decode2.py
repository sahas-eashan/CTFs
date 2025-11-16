import pathlib

code = pathlib.Path("chall.txt").read_text()
lines = code.split("\n")

# Each sequence like "01+a*3+a*2+a*4..." builds cumulative numbers:
# 0, 1, 1*10+3=13, 13*10+2=132, 132*10+4=1324, etc.
# But what we want are the final values that get pushed to stack

# Looking at the pattern: start with value, then repeatedly: *10 + digit
# The final numbers on the stack would be built up sequentially


def decode_arithmetic_sequence(seq: str) -> list[int]:
    """Decode a sequence like '01+a*3+a*2+a*4+a*5+' into numbers."""
    import re

    # Extract pattern: digit followed by optional 'a*' multiplier
    # Pattern: number is built as: val*10+next_digit repeatedly

    # Find all additions after initial value
    tokens = re.findall(r"([0-9a-f]+)", seq.lower())

    values = []
    current = 0

    for token in tokens:
        val = int(token, 16)
        if val == 10:  # 'a' means multiply by 10
            continue
        current = current * 10 + val
        values.append(current)

    return values


# Lines 7-11 are the data-building sequences
# Line 7: >~01+a*3+a*2+a*4+a*5+a*3+a*6+a*0+a*9+a*7+a*6v

sequences = [
    "01+a*3+a*2+a*4+a*5+a*3+a*6+a*0+a*9+a*7+a*6",  # line 7
    "8+a*8+a*8+a*4+a*3+a*5+a*8+a*2+a*1+a*5",  # line 8 (reading right-to-left: reversed)
    "9+a*8+a*7+a*7+a*3+a*2+a*3+a*8+a*9+a*9+a*8",  # line 9
    "0+a*7+a*5+a*3+a*6+a*9+a*8+a*8+a*1+a*6+a*10",  # line 10 (reversed)
    "a*3+a*6+a*6+a*6",  # line 11
]

print("Decoding arithmetic sequences as cumulative builds:\n")

all_ascii = []

for i, seq in enumerate(sequences, start=7):
    print(f"Line {i}: {seq}")

    # Build number step by step
    import re

    parts = re.split(r"[+*]", seq)

    current = 0
    values = []

    for part in parts:
        if not part or part == "a":
            continue

        val = int(part, 16) if part in "0123456789abcdef" else 0

        if val == 10:  # multiply by 10
            current *= 10
        else:
            current = current * 10 + val
            values.append(current)

    print(f"  Built values: {values}")

    # The FINAL value is what matters - but actually, reading the Fish code,
    # it pushes each intermediate? Let's try interpreting the final values as ASCII

    # Actually wait - looking at line 11: "a*3+a*6+a*6+a*6++>"
    # The ++ suggests we're adding things together
    # And the pattern `f1+6*%84*+o` suggests: (val % 16) * 84 + output

    # Let me reconsider: maybe each "+a*digit" pushes (digit) onto stack?
    # Let's extract just the digits that come after "a*" or standalone

    digit_pattern = []
    i = 0
    while i < len(seq):
        if seq[i : i + 2] == "a*" or seq[i] == "+":
            i += 2 if seq[i : i + 2] == "a*" else 1
            if i < len(seq) and seq[i] in "0123456789abcdef":
                digit_pattern.append(int(seq[i], 16))
        else:
            i += 1

    print(f"  Digit pattern: {digit_pattern}")

    # Try as raw ASCII
    try:
        ascii_str = "".join(chr(d + 48) for d in digit_pattern)  # +48 = '0'
        print(f"  As digit chars: {ascii_str}")

        # Or as direct ASCII
        ascii_str2 = "".join(chr(d * 10) for d in digit_pattern if d * 10 < 127)
        if ascii_str2:
            print(f"  As ASCII (d*10): {ascii_str2}")
    except:
        pass

    print()
