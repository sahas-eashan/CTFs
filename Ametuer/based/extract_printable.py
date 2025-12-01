import string

# Read base91-decoded binary
with open('flag2.bin', 'rb') as f:
    data = f.read()

# Extract printable ASCII runs of length >= 8
min_run = 8
runs = []
current = b''
for b in data:
    if chr(b) in string.printable:
        current += bytes([b])
    else:
        if len(current) >= min_run:
            runs.append(current)
        current = b''
if len(current) >= min_run:
    runs.append(current)

for i, run in enumerate(runs):
    print(f'Run {i}:', run)

# Save all runs to a file
with open('flag2_printable.txt', 'w', encoding='utf-8') as out:
    for run in runs:
        out.write(run.decode(errors='replace') + '\n')
print('Extracted printable ASCII runs to flag2_printable.txt')
