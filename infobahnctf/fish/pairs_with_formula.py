digits = "132453609765128534888987732389980753698816"

print("Applying (pair % 96) + 32 to pairs:\n")
flag_chars = []
i = 0
while i < len(digits) - 1:
    pair = digits[i:i+2]
    val = int(pair)
    result = (val % 96) + 32
    if 32 <= result < 128:
        char = chr(result)
        print(f"{pair} -> ({val} % 96) + 32 = {result} = '{char}'")
        flag_chars.append(char)
    i += 2

forward = ''.join(flag_chars)
reversed_flag = forward[::-1]

print(f"\nForward:  {forward}")
print(f"Reversed: {reversed_flag}")
print(f"\nWrapped: infobahn{{{reversed_flag}}}")
