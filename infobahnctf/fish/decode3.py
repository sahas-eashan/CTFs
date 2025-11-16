import pathlib

# Let me re-examine: maybe I need to read the values BACKWARDS from how they're built
# Or maybe the formula is different

# Looking at trace.py output: when it hit the output routine at step 6971,
# stack was [1, 121, 0, 0] then went to [122, 121, 50]
# And the routine is: :f1+6*%84*+o
# f=15, so f1+ = 16, *6 = 96
# So formula is: (val % 96) + 32

# But maybe the numbers aren't meant to be the cumulative builds?
# Maybe just the DIGITS themselves are the data?

# From the sequences, extract just the added digits:
seqs_raw = [
    "01+a*3+a*2+a*4+a*5+a*3+a*6+a*0+a*9+a*7+a*6",  # line 7
    "5+a*1+a*2+a*8+a*5+a*3+a*4+a*8+a*8+a*8",  # line 8 reversed
    "9+a*8+a*7+a*7+a*3+a*2+a*3+a*8+a*9+a*9+a*8",  # line 9
    "0+a*7+a*5+a*3+a*6+a*9+a*8+a*8+a*1+a*6+a*10",  # line 10 reversed
    "a*3+a*6+a*6+a*6",  # line 11
]

all_digits = []

for seq in seqs_raw:
    # Extract just the digits that are added (not multiplied)
    import re

    # Pattern: digit after + or at start, but not 'a' (which is 10)
    parts = seq.replace("a*", " ").replace("+", " ").split()
    for part in parts:
        if part and part not in ["a", "*", "+"]:
            try:
                val = int(part, 16)
                all_digits.append(val)
            except:
                pass

print(f"Extracted digits: {all_digits}")

# Try direct ASCII
print("\nDirect ASCII:")
try:
    direct = "".join(chr(d + 48) if d < 10 else chr(d + 87) for d in all_digits)
    print(f"  As chars: {direct}")
except:
    pass

# Try with offset
print("\nWith various offsets:")
for offset in [0, 32, 48, 87]:
    try:
        s = "".join(chr(d + offset) for d in all_digits if 0 <= d + offset < 128)
        print(f"  Offset {offset}: {s}")
    except:
        pass

# Try treating as two-digit ASCII codes
print("\nAs two-digit pairs:")
pairs = []
i = 0
while i < len(all_digits) - 1:
    val = all_digits[i] * 10 + all_digits[i + 1]
    if 32 <= val < 128:
        pairs.append(chr(val))
        i += 2
    else:
        i += 1
print(f"  {''.join(pairs)}")

# Try three-digit codes
print("\nAs three-digit pairs:")
trios = []
i = 0
while i < len(all_digits) - 2:
    val = all_digits[i] * 100 + all_digits[i + 1] * 10 + all_digits[i + 2]
    if 32 <= val < 128:
        trios.append(chr(val))
        i += 3
    else:
        i += 1
print(f"  {''.join(trios)}")
