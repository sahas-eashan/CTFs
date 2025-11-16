# Take each individual digit (0-9) and add 48 to get ASCII '0'-'9'
digits_str = "132453609765128534888987732389980753698816"

print("Converting each digit to its ASCII character equivalent:\n")
flag_chars = []
for digit_char in digits_str:
    digit_val = int(digit_char)
    ascii_val = digit_val + 48  # '0' starts at ASCII 48
    char = chr(ascii_val)
    print(f"{digit_char} -> {digit_val} + 48 = {ascii_val} = '{char}'")
    flag_chars.append(char)

forward = "".join(flag_chars)
reversed_flag = forward[::-1]

print(f"\nForward:  {forward}")
print(f"Reversed: {reversed_flag}")
print(f"\nWrapped: infobahn{{{reversed_flag}}}")
