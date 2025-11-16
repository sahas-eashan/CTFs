digits = "132453609765128534888987732389980753698816"

print("Treating as straight 2-digit ASCII (no formulas):\n")
flag_chars = []
i = 0
while i < len(digits) - 1:
    pair = digits[i : i + 2]
    val = int(pair)
    if 32 <= val < 128:
        char = chr(val)
        print(f"{pair} = {val} = '{char}'")
        flag_chars.append(char)
        i += 2
    else:
        print(f"{pair} = {val} (out of range)")
        i += 1

forward = "".join(flag_chars)
reversed_flag = forward[::-1]

print(f"\nForward:  {forward}")
print(f"Reversed: {reversed_flag}")
print(f"\nWrapped: infobahn{{{reversed_flag}}}")
