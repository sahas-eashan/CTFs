# Wait - looking at the title "This fish is swimming backward, can you reverse it?"
# Maybe I need to REVERSE the entire output!

flag_raw = ' -$aAU"XYWI&cPK$bQL$B'
reversed_flag = flag_raw[::-1]

print(f"Original: {flag_raw}")
print(f"Reversed: {reversed_flag}")
print(f"Wrapped: infobahn{{{reversed_flag}}}")
