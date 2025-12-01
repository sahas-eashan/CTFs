with open('chal','rb') as f:
    data = f.read()
needle = b"you can never have too much zig pwn.\n"
print(hex(data.find(needle)))
