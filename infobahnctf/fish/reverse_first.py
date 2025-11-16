# The reversed string "@XE57bYGIWYX"U<Aa<5H=" doesn't look right either
# Let me try: what if the ENTIRE string needs more processing?

# Looking back at "This fish is swimming backward" - maybe I need to
# reverse the DIGIT STRING first, THEN decode?

digits_str = "132453609765128534888987732389980753698816"
reversed_digits = digits_str[::-1]

print(f"Original digits: {digits_str}")
print(f"Reversed digits: {reversed_digits}")
print()

print("Decoding REVERSED digit string as 2-digit ASCII:\n")

flag_chars = []
i = 0
while i < len(reversed_digits) - 1:
    pair = reversed_digits[i : i + 2]
    val = int(pair)

    if 32 <= val < 128:
        char = chr(val)
        print(f"  {pair} = {val} = '{char}'")
        flag_chars.append(char)
        i += 2
    else:
        print(f"  {pair} = {val} (skip)")
        i += 1

flag = "".join(flag_chars)
print(f"\nDecoded: {flag}")
print(f"\nWrapped: infobahn{{{flag}}}")
