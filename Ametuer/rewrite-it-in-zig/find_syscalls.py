with open('chal', 'rb') as f:
    data = f.read()
needle = b"\x0f\x05"
offsets = []
start = 0
while True:
    idx = data.find(needle, start)
    if idx == -1:
        break
    offsets.append(idx)
    start = idx + 1
base = 0x1000000
for i, off in enumerate(offsets[:50]):
    print(f"[{i}] file_off=0x{off:x} vaddr=0x{base + off:x}")
print(f"total syscalls: {len(offsets)}")
