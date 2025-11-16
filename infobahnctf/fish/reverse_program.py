with open('chall.txt', 'r') as f:
    lines = f.readlines()

with open('chall_reversed.txt', 'w') as f:
    for line in lines:
        # Remove newline, reverse, add newline back
        reversed_line = line.rstrip('\n')[::-1] + '\n'
        f.write(reversed_line)

print("Created chall_reversed.txt with each line reversed")

# Also create fully reversed (lines in reverse order AND each line reversed)
with open('chall_fully_reversed.txt', 'w') as f:
    for line in reversed(lines):
        reversed_line = line.rstrip('\n')[::-1] + '\n'
        f.write(reversed_line)

print("Created chall_fully_reversed.txt with lines and characters reversed")
