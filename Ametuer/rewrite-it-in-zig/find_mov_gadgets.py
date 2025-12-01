with open('chal','rb') as f:
    data=f.read()

patterns = {
    'mov rdi, rax; ret': b'\x48\x89\xc7\xc3',
    'mov rsi, rax; ret': b'\x48\x89\xc6\xc3',
    'mov rdx, rax; ret': b'\x48\x89\xc2\xc3',
}
for name, pat in patterns.items():
    idx = data.find(pat)
    print(name, hex(idx) if idx != -1 else idx)
