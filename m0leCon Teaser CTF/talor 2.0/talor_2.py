#!/usr/bin/env python3
from pwn import *
import json


def make_collision(length: int = 4):
    """
    Build two distinct byte strings of the given length that collide under h.

    All arithmetic inside the sponge works modulo 59, so bytes that differ by
    a multiple of 59 behave identically. We pick the all-zero string and a copy
    where the first byte is increased by 59; both hash to the same value while
    remaining short and easy to transmit.
    """

    base = bytes([0] * length)
    tweaked = bytes([59] + [0] * (length - 1))
    assert base != tweaked
    return base, tweaked


def solve():
    conn = remote("talor2.challs.m0lecon.it", 22972)

    m1, m2 = make_collision()
    m1_hex = m1.hex().encode()
    m2_hex = m2.hex().encode()

    for round_idx in range(10):
        conn.recvuntil(b"rc = ")
        rc_line = conn.recvline().strip()
        try:
            rc = json.loads(rc_line)
            log.info(f"Round {round_idx+1}: received rc[{len(rc)}]")
        except Exception:
            log.warning(f"Round {round_idx+1}: unexpected rc line {rc_line!r}")

        conn.sendlineafter(b"M1: ", m1_hex)
        conn.sendlineafter(b"M2: ", m2_hex)

    flag = conn.recvall(timeout=2).decode().strip()
    log.success(flag)
    conn.close()


if __name__ == "__main__":
    solve()
