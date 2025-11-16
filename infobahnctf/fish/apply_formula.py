# Looking at final_decode.py output, the cumulative numbers were:
cumulative = [
    1,
    103,
    10302,
    1030204,
    103020405,
    10302040503,
    1030204050306,
    103020405030600,
    10302040503060009,
    1030204050306000907,
    103020405030600090706,
    5,
    501,
    50102,
    5010208,
    501020805,
    50102080503,
    5010208050304,
    501020805030408,
    50102080503040808,
    5010208050304080808,
    9,
    908,
    90807,
    9080707,
    908070703,
    90807070302,
    9080707030203,
    908070703020308,
    90807070302030809,
    9080707030203080909,
    908070703020308090908,
    0,
    7,
    705,
    70503,
    7050306,
    705030609,
    70503060908,
    7050306090808,
    705030609080801,
    70503060908080106,
    7050306090808010616,
    3,
    306,
    30606,
    3060606,
]

# Use formula (val % 96) + 32
flag_chars = []
for val in cumulative:
    ascii_val = (val % 96) + 32
    if 32 <= ascii_val < 128:
        flag_chars.append(chr(ascii_val))

flag = "".join(flag_chars)
print(f"Forward: {flag}")

reversed_flag = flag[::-1]
print(f"Reversed: {reversed_flag}")

print(f"\nWrapped: infobahn{{{reversed_flag}}}")
