#!/usr/bin/env python3
"""
addition3 solver for AmateursCTF

Attack:
- Server encrypts: m = (flag << 512) + r + scramble (mod n) where r is 512-bit random
- Returns: c = m^3 mod n with e=3
- When scramble = -(guess << 512), plaintext becomes: t = (flag - guess) << 512 + r
- If guess == flag, then t = r (just 512 bits)
- Since r^3 << n (512*3 = 1536 bits << 2048 bits), c = r^3 is a perfect cube!
- We detect correct bytes when ciphertext is a perfect integer cube

Strategy: Byte-by-byte brute force using perfect cube detection
"""

from Crypto.Util.number import bytes_to_long, long_to_bytes
from pwn import *
import sys
import string

context.log_level = "info"


def icbrt(n):
    """Integer cube root using Newton's method for speed"""
    if n == 0:
        return 0
    if n < 8:
        return 1

    # Initial guess using bit length
    x = 1 << ((n.bit_length() + 2) // 3)

    # Newton iterations: x_new = (2*x + n/x^2) / 3
    while True:
        x_new = (2 * x + n // (x * x)) // 3
        if x_new >= x:
            break
        x = x_new

    # Verify and adjust
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
    # Format: n, e = (123..., 3)
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


def solve_remote(host="amt.rs", port=35077):
    """Solve the challenge by recovering flag byte-by-byte"""
    io = remote(host, port)

    try:
        n, e = get_params(io)
        log.info(f"Connected! n has {n.bit_length()} bits, e = {e}")

        # Known prefix
        prefix = b"amateursCTF{"
        known = prefix

        log.info(f"Starting with known prefix: {known.decode()}")

        # Recover each byte
        for pos in range(len(prefix), 52):
            log.info(f"[{pos}/52] Searching byte {pos}...")

            found = False

            # Try printable ASCII
            candidates = string.printable.encode()

            for byte_val in candidates:
                # Build test flag: known + guess + null padding
                test = known + bytes([byte_val]) + b'\x00' * (51 - pos)
                guess = bytes_to_long(test)

                # Scramble to cancel flag if guess is correct
                scramble = -(guess << 512)

                try:
                    c = query(io, scramble)
                except:
                    log.error("Connection lost, reconnecting...")
                    io.close()
                    io = remote(host, port)
                    n, e = get_params(io)
                    c = query(io, scramble)

                # Check if perfect cube (indicates correct guess)
                if is_perfect_cube(c):
                    known = known + bytes([byte_val])
                    char = chr(byte_val) if 32 <= byte_val < 127 else f"\\x{byte_val:02x}"
                    log.success(f"Byte {pos} = '{char}' [PERFECT CUBE]")
                    log.info(f"Current flag: {known.decode('ascii', errors='replace')}")
                    found = True
                    break

                # Also check n-c (edge case for modular wrapping)
                if is_perfect_cube(n - c):
                    known = known + bytes([byte_val])
                    char = chr(byte_val) if 32 <= byte_val < 127 else f"\\x{byte_val:02x}"
                    log.success(f"Byte {pos} = '{char}' [COMPLEMENT CUBE]")
                    log.info(f"Current flag: {known.decode('ascii', errors='replace')}")
                    found = True
                    break

            if not found:
                log.error(f"Failed to find byte {pos}!")
                log.info(f"Partial flag: {known}")
                break

        log.success(f"\n{'='*70}")
        log.success(f"FLAG: {known.decode('ascii', errors='replace')}")
        log.success(f"{'='*70}\n")

        return known

    finally:
        io.close()


def test_local():
    """Test perfect cube detection locally"""
    from Crypto.Util.number import getPrime
    from random import getrandbits

    log.info("Testing perfect cube detection...")

    # Test flag (exactly 52 bytes)
    flag = b"amateursCTF{test_flag_for_local_testing_only_0k????}"
    assert len(flag) == 52

    F = bytes_to_long(flag)
    FLAG_SHIFT = F << 512

    # Simulate RSA params
    n = getPrime(1024) * getPrime(1024)
    e = 3

    log.info(f"Flag: {flag}")
    log.info(f"n bits: {n.bit_length()}")
    log.info(f"n^(1/3) bits: {n.bit_length() // 3}")

    # Test 1: Correct guess should give perfect cube
    log.info("\n=== Test 1: Correct flag guess ===")
    r = getrandbits(512)
    scramble = -(F << 512)
    t = (FLAG_SHIFT + r + scramble) % n
    c = pow(t, e, n)

    log.info(f"t (should be ~512 bits): {t.bit_length()} bits")
    log.info(f"Is perfect cube: {is_perfect_cube(c)}")

    if is_perfect_cube(c):
        recovered_t = icbrt(c)
        log.success(f"✓ Correctly detected as perfect cube!")
        log.info(f"Recovered t matches: {recovered_t == t}")

    # Test 2: Wrong guess should NOT give perfect cube
    log.info("\n=== Test 2: Wrong flag guess ===")
    wrong_flag = b"amateursCTF{wr0ng_fl4g_f0r_testing_purp0ses!!!!}"
    assert len(wrong_flag) == 52
    W = bytes_to_long(wrong_flag)

    r = getrandbits(512)
    scramble = -(W << 512)
    t = (FLAG_SHIFT + r + scramble) % n
    c = pow(t, e, n)

    log.info(f"t (should be ~928 bits): {t.bit_length()} bits")
    log.info(f"Is perfect cube: {is_perfect_cube(c)}")

    if not is_perfect_cube(c):
        log.success(f"✓ Correctly rejected wrong guess!")

    # Test 3: Byte-by-byte recovery simulation
    log.info("\n=== Test 3: Byte-by-byte recovery ===")
    known = b"amateursCTF{"

    for pos in range(len(known), min(len(known) + 5, 52)):  # Test first 5 bytes after prefix
        correct_byte = flag[pos]
        found = False

        for test_byte in range(32, 127):
            test_flag = known + bytes([test_byte]) + b'\x00' * (51 - pos)
            guess = bytes_to_long(test_flag)

            r = getrandbits(512)
            scramble = -(guess << 512)
            t = (FLAG_SHIFT + r + scramble) % n
            c = pow(t, e, n)

            if is_perfect_cube(c):
                if test_byte == correct_byte:
                    log.success(f"Byte {pos}: '{chr(test_byte)}' [OK]")
                    known += bytes([test_byte])
                    found = True
                    break
                else:
                    log.error(f"False positive at byte {pos}!")

        if not found:
            log.error(f"Failed to find byte {pos}!")
            break

    log.info(f"\nRecovered: {known}")


if __name__ == "__main__":
    if "--test" in sys.argv:
        test_local()
    else:
        # Default: connect to remote
        flag = solve_remote()
        print(f"\n[+] FINAL FLAG: {flag.decode('ascii', errors='replace')}")
