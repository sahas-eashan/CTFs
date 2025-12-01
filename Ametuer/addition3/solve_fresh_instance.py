#!/usr/bin/env python3
"""
Solve addition3 with fresh server instance
Port: 38639 (expires in ~10 minutes)

Strategy: Try perfect cube detection with byte-by-byte recovery
Since this is a fresh instance, we have limited time!
"""

from Crypto.Util.number import bytes_to_long, long_to_bytes
from pwn import *
import string

context.log_level = "info"


def icbrt(n):
    """Fast integer cube root"""
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


def test_guess_multiple(io, n, guess_bytes, samples=20):
    """Test a guess with multiple samples to increase hit probability"""
    guess = bytes_to_long(guess_bytes)
    scramble = -(guess << 512)

    cube_count = 0

    for i in range(samples):
        try:
            c = query(io, scramble)

            if is_perfect_cube(c):
                cube_count += 1

            if is_perfect_cube(n - c):
                cube_count += 1

        except Exception as ex:
            log.warning(f"Query {i} failed: {ex}")
            return cube_count

    return cube_count


def solve(host="amt.rs", port=38639):
    """Solve with fresh instance"""
    io = remote(host, port)

    try:
        n, e = get_params(io)
        log.info(f"Connected! n={n.bit_length()} bits, e={e}")

        prefix = b"amateursCTF{"
        known = prefix

        log.info(f"Starting with: {known.decode()}")

        # Try to find each byte
        for pos in range(len(prefix), 52):
            log.info(f"\n[{pos}/52] Byte {pos}...")

            best_char = None
            best_score = -1

            # Common flag characters
            candidates = b"_}abcdefghijklmnopqrstuvwxyz0123456789"

            for byte_val in candidates:
                test = known + bytes([byte_val]) + b'\x00' * (51 - pos)

                char_display = chr(byte_val)

                # Test with multiple samples (increases probability of hitting the perfect cube)
                score = test_guess_multiple(io, n, test, samples=10)

                log.info(f"  '{char_display}': score={score}")

                if score > best_score:
                    best_score = score
                    best_char = byte_val

                if score >= 1:  # Found at least one perfect cube!
                    log.success(f"Byte {pos} = '{char_display}' (score={score})")
                    known = known + bytes([byte_val])
                    break

            if not known.endswith(bytes([best_char])):
                if best_score > 0:
                    log.success(f"Best guess: '{chr(best_char)}' (score={best_score})")
                    known = known + bytes([best_char])
                else:
                    log.error(f"No good guess for byte {pos}!")
                    break

            log.info(f"Progress: {known.decode('ascii', errors='replace')}")

        log.success(f"\n{'='*70}")
        log.success(f"FLAG: {known.decode('ascii', errors='replace')}")
        log.success(f"{'='*70}")

        return known

    finally:
        io.close()


if __name__ == "__main__":
    flag = solve()
    print(f"\n[+] FINAL: {flag.decode('ascii', errors='replace')}")
