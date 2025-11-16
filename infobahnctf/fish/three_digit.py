digits_str = "132453609765128534888987732389980753698816"

# Split into groups of 3
groups = []
for i in range(0, len(digits_str), 3):
    groups.append(digits_str[i : i + 3])

print("Three-digit groups:", groups)
print()

flag_chars = []
for group in groups:
    if len(group) == 3:
        val = int(group)
        if 32 <= val < 128:
            char = chr(val)
            print(f"{group} -> {val} -> '{char}'")
            flag_chars.append(char)
        else:
            print(f"{group} -> {val} (out of range)")

flag = "".join(flag_chars)
print(f"\nDecoded: {flag}")
print(f"Reversed: {flag[::-1]}")
print(f"\nWrapped: infobahn{{{flag[::-1]}}}")
