#!/usr/bin/env python3
"""
Debug version - test perfect cube detection
"""

from Crypto.Util.number import bytes_to_long, long_to_bytes
from pwn import *

context.log_level = "info"


def icbrt(n):
    """Integer cube root using Newton's method"""
    if n == 0:
        return 0
    if n < 8:
        return 1

    x = 1 << ((n.bit_length() + 2) // 3)

    while True:
        x_new = (2 * x + n // (x * x)) // 3
        if x_new >= x:
            break
        x = x_new

    while x**3 > n:
        x -= 1
    while (x + 1)**3 <= n:
        x += 1

    return x


def is_perfect_cube(c):
    """Check if c is a perfect cube"""
    if c == 0:
        return True
    root = icbrt(c)
    return root**3 == c


def get_params(io):
    """Parse n, e from server"""
    line = io.recvline().decode()
    parts = line.split("=")[1].strip()
    n_str, e_str = parts.strip("()").split(",")
    n = int(n_str.strip())
    e = int(e_str.strip())
    return n, e


def query(io, scramble):
    """Send scramble and get ciphertext"""
    io.recvuntil(b"scramble the flag: ")
    io.sendline(str(scramble).encode())
    io.recvuntil(b"scrambling...\n")
    line = io.recvline().decode()
    c = int(line.split("=")[1].strip())
    return c


# Connect and test
io = remote("amt.rs", 35077)

try:
    n, e = get_params(io)
    log.info(f"n = {n}")
    log.info(f"n bits = {n.bit_length()}")
    log.info(f"n^(1/3) bits = {n.bit_length() // 3}")

    # Test 1: Try scramble = 0
    log.info("\n=== Test 1: scramble = 0 ===")
    c1 = query(io, 0)
    log.info(f"c bits = {c1.bit_length()}")
    log.info(f"Is perfect cube: {is_perfect_cube(c1)}")
    log.info(f"Is (n-c) perfect cube: {is_perfect_cube(n - c1)}")

    # Test 2: Try a known prefix guess
    log.info("\n=== Test 2: Known prefix ===")
    io.close()
    io = remote("amt.rs", 35077)
    n, e = get_params(io)

    test = b"amateursCTF{" + b"\x00" * 40
    guess = bytes_to_long(test)
    scramble = -(guess << 512)

    log.info(f"Test flag: {test[:20]}...")
    log.info(f"Scramble bits: {abs(scramble).bit_length()}")

    c2 = query(io, scramble)
    log.info(f"c bits = {c2.bit_length()}")
    log.info(f"Is perfect cube: {is_perfect_cube(c2)}")
    log.info(f"Is (n-c) perfect cube: {is_perfect_cube(n - c2)}")

    if is_perfect_cube(c2):
        r = icbrt(c2)
        log.info(f"Recovered r bits: {r.bit_length()}")
        log.info(f"r = {r}")

    # Test 3: Try with a wrong first character after prefix
    log.info("\n=== Test 3: Wrong character ===")
    io.close()
    io = remote("amt.rs", 35077)
    n, e = get_params(io)

    test = b"amateursCTF{X" + b"\x00" * 39
    guess = bytes_to_long(test)
    scramble = -(guess << 512)

    c3 = query(io, scramble)
    log.info(f"c bits = {c3.bit_length()}")
    log.info(f"Is perfect cube: {is_perfect_cube(c3)}")
    log.info(f"Is (n-c) perfect cube: {is_perfect_cube(n - c3)}")

finally:
    io.close()
