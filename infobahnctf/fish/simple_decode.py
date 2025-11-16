# The challenge says "320" - maybe this is the KEY for decoding?
# Or maybe I need to look at what the program ACTUALLY does with that input

# Looking at the trace output earlier, when it hit 121:
# It went to coordinates and started doing operations
# The formula on line 11 is: :f1+6*%84*+o
# Which is: duplicate, (15+1)*6 = 96, modulo 96, 8*4=32, add 32, output

# But wait - looking at the input "320" - that's a NUMBER
# And the program checks if counter % 121 == 0
# So it runs 121 times before outputting

# Actually, let me just directly decode the digit string as 3-digit ASCII
# BUT using the transformation first

digits_str = "132453609765128534888987732389980753698816"

print(f"Digit string: {digits_str}")
print(f"Length: {len(digits_str)}")
print()

# Try interpreting as: take each digit, build 3-digit numbers
flag_chars = []

# Method 1: Groups of 3 with modulo formula
print("Method 1: 3-digit groups with (val % 96) + 32:")
for i in range(0, len(digits_str) - 2, 3):
    group = digits_str[i : i + 3]
    val = int(group)
    ascii_val = (val % 96) + 32
    if 32 <= ascii_val < 128:
        char = chr(ascii_val)
        print(f"  {group} -> {val} % 96 + 32 = {ascii_val} = '{char}'")
        flag_chars.append(char)

flag = "".join(flag_chars)
print(f"\nForward: {flag}")
print(f"Reversed: {flag[::-1]}")
print(f"\nWrapped: infobahn{{{flag[::-1]}}}")
print()

# Method 2: Maybe it's simpler - just the digits themselves represent ASCII directly
print("Method 2: Digits as 2-digit ASCII (e.g., 97 = 'a'):")
flag2 = []
for i in range(0, len(digits_str) - 1, 2):
    pair = digits_str[i : i + 2]
    val = int(pair)
    if 32 <= val < 128:
        char = chr(val)
        print(f"  {pair} = {val} = '{char}'")
        flag2.append(char)
    else:
        print(f"  {pair} = {val} (skip)")

flag2_str = "".join(flag2)
print(f"\nForward: {flag2_str}")
print(f"Reversed: {flag2_str[::-1]}")
