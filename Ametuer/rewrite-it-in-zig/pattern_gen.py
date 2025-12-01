from pwn import cyclic

with open('pattern', 'wb') as f:
    f.write(cyclic(400))
