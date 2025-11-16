# What if each DIGIT (0-9) needs the formula applied?
# Lines 7-10 build up these sequences:
# 0,1,3,2,4,5,3,6,0,9,7,6
# 5,1,2,8,5,3,4,8,8,8,9,8
# 9,8,7,7,3,2,3,8,9,9,8
# 10,6,1,8,8,9,6,3,5,7,0

# Formula: (val % 96) + 32

sequences = [
    [0, 1, 3, 2, 4, 5, 3, 6, 0, 9, 7, 6],
    [5, 1, 2, 8, 5, 3, 4, 8, 8, 8, 9, 8],
    [9, 8, 7, 7, 3, 2, 3, 8, 9, 9, 8],
    [10, 6, 1, 8, 8, 9, 6, 3, 5, 7, 0],
]

print("Applying (val % 96) + 32 to each digit:\n")

all_chars = []
for seq_num, seq in enumerate(sequences, 1):
    print(f"Sequence {seq_num}:")
    for val in seq:
        result = (val % 96) + 32
        char = chr(result)
        print(f"  {val} -> ({val} % 96) + 32 = {result} = '{char}'")
        all_chars.append(char)
    print()

forward = "".join(all_chars)
reversed_flag = forward[::-1]

print(f"Forward: {forward}")
print(f"Reversed: {reversed_flag}")
print(f"\nWrapped: infobahn{{{reversed_flag}}}")
