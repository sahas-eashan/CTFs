with open('chal','rb') as f:
    data = f.read()

needle = b'\x5f\xc3'
pos = data.find(needle)
results = []
while pos != -1:
    results.append(pos)
    pos = data.find(needle, pos + 1)

print('pop rdi; ret occurrences:', len(results))
print(results[:20])
