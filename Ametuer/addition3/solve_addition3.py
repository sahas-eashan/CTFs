#!/usr/bin/env python3
"""
addition3 solver for AmateursCTF

Strategy:
- The server encrypts m = (flag << 512) + random_512_bits + scramble with RSA e=3
- We can choose scramble to make m small enough that m^3 < n
- When m^3 < n, we can take the integer cube root directly to recover m
- By binary searching the flag value via scramble adjustments, we find when
  the ciphertext becomes a perfect cube (indicating our guess is close)
- Once we recover m, we extract flag = (m - random_bits) >> 512

Usage:
    python solve_addition3.py              # Connect to remote
    python solve_addition3.py --test       # Test locally
"""

from Crypto.Util.number import bytes_to_long, long_to_bytes, getPrime
from pwn import *
import sys

context.log_level = "info"


def icbrt(n):
    """Integer cube root via binary search"""
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
    """Check if c is a perfect cube"""
    if c == 0:
        return True
    root = icbrt(c)
    return root**3 == c


def query_remote(io, scramble):
    """Send scramble to server and get back n, e, c"""
    io.recvuntil(b"scramble the flag: ")
    io.sendline(str(scramble).encode())
    io.recvuntil(b"scrambling...\n")
    line = io.recvline().decode()
    # Parse: c = 123456...
    c = int(line.split("=")[1].strip())
    return c


def get_n_e(io):
    """Parse n, e from initial server response"""
    line = io.recvline().decode()
    # Parse: n, e = (123..., 3)
    parts = line.split("=")[1].strip()
    n_str, e_str = parts.strip("()").split(",")
    n = int(n_str.strip())
    e = int(e_str.strip())
    return n, e


def solve_remote(host="amt.rs", port=37555):
    """Solve the remote challenge"""
    io = remote(host, port)

    try:
        # Get n, e
        n, e = get_n_e(io)
        log.info(f"n = {n}")
        log.info(f"e = {e}")
        log.info(f"n bits = {n.bit_length()}")

        # Strategy: when we send scramble = -(guess << 512),
        # the plaintext becomes: t = (FLAG_SHIFT + r + scramble) mod n
        #                           = (FLAG_SHIFT - guess<<512 + r) mod n
        # If guess == FLAG exactly, then t = r (a 512-bit random number)
        # Since r < 2^512 << n^(1/3) ~= 2^683, we get c = r^3 which is a perfect cube

        # Binary search for each byte of the flag
        prefix = b"amateursCTF{"
        known = prefix

        log.info(f"Starting search with prefix: {known}")

        # For each remaining byte position
        for byte_pos in range(len(prefix), 52):
            log.info(f"Searching byte {byte_pos}/52")

            found = False
            # Try printable ASCII characters
            for byte_val in range(32, 127):
                # Build test flag: known bytes + this guess + padding
                test_flag = known + bytes([byte_val]) + b"\x00" * (51 - byte_pos)
                guess = bytes_to_long(test_flag)

                # Send scramble to make plaintext = r (if guess is correct)
                scramble = -(guess << 512)
                c = query_remote(io, scramble)

                # Check if result is a perfect cube (t is small)
                if is_perfect_cube(c):
                    known = known + bytes([byte_val])
                    log.success(
                        f"Byte {byte_pos} = {repr(chr(byte_val))} [perfect cube]"
                    )
                    found = True
                    break

                # Also check complement (in case we overshot slightly)
                if is_perfect_cube(n - c):
                    if byte_val > 32:
                        known = known + bytes([byte_val - 1])
                        log.success(
                            f"Byte {byte_pos} = {repr(chr(byte_val-1))} [complement cube]"
                        )
                        found = True
                        break

            if not found:
                # Fallback: try common flag characters
                log.warning(
                    f"Standard search failed for byte {byte_pos}, trying common chars"
                )
                for ch in b"_0123456789abcdefghijklmnopqrstuvwxyz}":
                    test_flag = known + bytes([ch]) + b"\x00" * (51 - byte_pos)
                    guess = bytes_to_long(test_flag)
                    scramble = -(guess << 512)
                    c = query_remote(io, scramble)

                    if is_perfect_cube(c) or is_perfect_cube(n - c):
                        known = known + bytes([ch])
                        log.success(f"Byte {byte_pos} = {repr(chr(ch))} [fallback]")
                        found = True
                        break

            if not found:
                log.error(f"Failed to find byte {byte_pos}!")
                break

        log.success(f"Recovered flag: {known}")
        return known

    finally:
        io.close()


def solve_local():
    """Test the solver logic locally"""
    from random import getrandbits

    # Simulate local challenge
    flag = b"amateursCTF{test_flag_for_local_testing_only_ok?}"
    assert len(flag) == 52

    F = bytes_to_long(flag)
    FLAG_SHIFT = F << 512

    n = getPrime(1024) * getPrime(1024)
    e = 3

    log.info(f"Local test with flag: {flag}")
    log.info(f"n bits: {n.bit_length()}")

    # Test perfect cube detection
    for delta in [0, 1, -1, 1 << 10, -(1 << 10)]:
        guess = F + delta
        r = getrandbits(512)
        S = -(guess << 512)
        t = (FLAG_SHIFT + r + S) % n
        c = pow(t, e, n)

        is_cube = is_perfect_cube(c)
        is_complement_cube = is_perfect_cube(n - c)

        log.info(
            f"delta={delta:20d} | t_bits={t.bit_length():4d} | cube={is_cube} | n-c_cube={is_complement_cube}"
        )

        if is_cube and t < (1 << 700):
            # Can recover directly
            recovered_t = icbrt(c)
            if recovered_t == t:
                recovered_flag = (recovered_t - r) >> 512
                log.success(f"Direct recovery: {long_to_bytes(recovered_flag)}")


if __name__ == "__main__":
    if "--test" in sys.argv:
        solve_local()
    else:
        flag = solve_remote()
        print(f"\n[+] FLAG: {flag.decode()}")
