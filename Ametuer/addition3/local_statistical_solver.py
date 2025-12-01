#!/usr/bin/env python3
"""
Statistical local solver for addition3

This script simulates the challenge locally and uses multiple samples per flag guess.
For each guess, it collects N ciphertexts and counts how many are perfect cubes.
The correct flag guess will yield a much higher cube count than incorrect guesses.
"""

from Crypto.Util.number import bytes_to_long, long_to_bytes, getPrime
from random import getrandbits, seed
import string

seed(123)

# Simulate challenge parameters
flag = b"amateursCTF{test_flag_for_local_testing_only_ok?}".ljust(52, b"!")
assert len(flag) == 52
F = bytes_to_long(flag)
FLAG_SHIFT = F << 512
n = getPrime(1024) * getPrime(1024)


# Helper: integer cube root
def icbrt(n):
    if n == 0:
        return 0
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid**3 <= n:
            lo = mid
        else:
            hi = mid - 1
    return lo


def is_perfect_cube(c):
    root = icbrt(c)
    return root**3 == c


# Statistical test for a flag guess
def test_guess(guess_bytes, num_samples=10):
    guess = bytes_to_long(guess_bytes)
    scramble = -(guess << 512)
    cube_count = 0
    for _ in range(num_samples):
        r = getrandbits(512)
        t = (FLAG_SHIFT + r + scramble) % n
        c = pow(t, 3, n)
        if is_perfect_cube(c):
            cube_count += 1
    return cube_count


# Recover flag byte-by-byte
prefix = b"amateursCTF{"
known = prefix

for byte_pos in range(len(prefix), 52):
    best_byte = None
    best_score = -1
    for b in range(32, 127):
        test_flag = known + bytes([b]) + b"\x00" * (51 - byte_pos)
        score = test_guess(test_flag, num_samples=10)
        if score > best_score:
            best_score = score
            best_byte = b
    known += bytes([best_byte])
    print(f"Byte {byte_pos}: {chr(best_byte)} (cube count: {best_score})")

print(f"\nRecovered flag: {known}")
