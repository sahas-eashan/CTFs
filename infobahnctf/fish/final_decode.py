import pathlib

# The output formula from line 11: (value % 96) + 32
# So I need the final values that are built and output

# Reading the trace earlier: at step 6971 when modulo hit zero,
# the stack was [1, 121, 0, 0] then it computed stuff

# Looking at lines 7-11, these build up large numbers through multiplication
# Line 7: 01+a*3+a*2+a*4+a*5+a*3+a*6+a*0+a*9+a*7+a*6
# This computes: 1, 13, 132, 1324, 13245, 132453, 1324536, 13245360, 132453609, 1324536097, 13245360976

# But then line 11 has the output: :f1+6*%84*+o
# Which is: (val % ((15+1)*6)) + (8*4) = (val % 96) + 32

values_line7 = [
    1,
    13,
    132,
    1324,
    13245,
    132453,
    1324536,
    13245360,
    132453609,
    1324536097,
    13245360976,
]
values_line8 = []  # Need to compute backwards since it's <

# Actually, let me trace what the program pushes on stack
# Line 7 reads: >~01+a*3+a*2+a*4+a*5+a*3+a*6+a*0+a*9+a*7+a*6v
# ~ pops, 0 pushes 0, 1 pushes 1, + adds -> 1
# a pushes 10, * multiplies -> 10
# 3 pushes 3, + adds -> 13
# a pushes 10, * multiplies -> 130
# 2 pushes 2, + adds -> 132
# etc.

# Then v goes down, <  goes left on line 8
# Line 8: v*a+8*a+8*a+8*a+4*a+3*a+5*a+8*a+2*a+1*a+5*a+<
# Reading LEFT to RIGHT but BACKWARDS in the code
# So: 5 +a* 1 +a* 2 +a* 8 +a* 5 +a* 3 +a* 4 +a* 8 +a* 8 +a* 8 +a* v
# = 5, 5*10+1=51, 512, 5128, 51285, 512853, 5128534, 51285348, 512853488, 5128534888

# Then continues with more sequences...

# Let me compute all the numbers:


def build_numbers_forward(seq_str):
    """Build numbers from a sequence like '01+a*3+a*2+...'"""
    import re

    tokens = re.findall(r"[0-9a-f]+|[+*~]", seq_str.lower())

    current = 0
    numbers = []

    for token in tokens:
        if token == "~":
            continue  # skip
        elif token == "+":
            continue
        elif token == "*":
            continue
        elif token == "a":
            current *= 10
        else:
            val = int(token, 16)
            if val == 10:  # 'a'
                current *= 10
            else:
                current = current * 10 + val
                numbers.append(current)

    return numbers


# Extract sequences (removing directional markers)
seqs = [
    "01+a*3+a*2+a*4+a*5+a*3+a*6+a*0+a*9+a*7+a*6",  # line 7 forward
    "5+a*1+a*2+a*8+a*5+a*3+a*4+a*8+a*8+a*8",  # line 8 reversed
    "9+a*8+a*7+a*7+a*3+a*2+a*3+a*8+a*9+a*9+a*8",  # line 9 forward
    "0+a*7+a*5+a*3+a*6+a*9+a*8+a*8+a*1+a*6+a*10",  # line 10 reversed
    "a*3+a*6+a*6+a*6",  # line 11 forward
]

all_values = []

for i, seq in enumerate(seqs):
    nums = build_numbers_forward(seq)
    print(f"Sequence {i}: {nums}")
    all_values.extend(nums)

print(f"\nAll values: {all_values}")
print(f"\nConverting to ASCII using (val % 96) + 32:")

flag_chars = []
for val in all_values:
    ascii_val = (val % 96) + 32
    flag_chars.append(chr(ascii_val))
    print(f"  {val} -> {val % 96} + 32 = {ascii_val} = '{chr(ascii_val)}'")

flag = "".join(flag_chars)
print(f"\nDecoded flag: {flag}")
print(f"\nWrapped: infobahn{{{flag}}}")
