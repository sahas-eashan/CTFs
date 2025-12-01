import sys

offset = int(sys.argv[1], 0) if len(sys.argv) > 1 else 0
length = int(sys.argv[2], 0) if len(sys.argv) > 2 else 0x40
with open('chal', 'rb') as f:
    f.seek(offset)
    data = f.read(length)
print(data)
