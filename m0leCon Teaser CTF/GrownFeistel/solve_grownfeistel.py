#!/usr/bin/env python3
"""
GrownFeistel - Hash Collision Challenge

The hash uses a Feistel cipher in a compression mode similar to Davies-Meyer.
We need to find collision pairs.

Key observation: The padding includes message length, so different-length
messages will have different padded forms.

Attack strategies:
1. Birthday attack on short messages
2. Exploit structural weakness in the Feistel construction
3. Same-length messages that produce identical hashes

Since this is based on a block cipher (likely secure), we need birthday paradox.
With 128-bit output, birthday bound is 2^64 operations (too much).

BUT - we only need 2 collision pairs, not break the whole hash!
And we control the IV per round (server provides it).

Let me try:
- Empty message vs single byte
- Minimal different messages
"""

from pwn import *
import sys, os
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))

# Import the hash function (avoid running main)
import importlib.util
spec = importlib.util.spec_from_file_location("gf", "grown_feistel.py")
gf = importlib.util.module_from_spec(spec)

# Don't execute, just load functions
exec(open("grown_feistel.py").read().split("if __name__")[0], gf.__dict__)

def find_collision(iv):
    """
    Find hash collision for given IV.

    Strategy: Try many short messages and look for hash collision.
    With birthday paradox, expect collision after sqrt(2^128) ≈ 2^64 (too much!)

    But maybe there's a weakness! Let's try simple messages first.
    """

    # Try various short messages
    hashes = {}

    # Strategy 1: Empty and short messages
    messages_to_try = [
        b"",
        b"\x00",
        b"\x01",
        b"\xff",
        b"\x00\x00",
        b"\x01\x01",
        b"\xff\xff",
        b"A",
        b"AA",
        b"AAA",
        b"test",
        b"flag",
    ]

    for msg in messages_to_try:
        h = gf.hash(msg, iv)
        h_tuple = tuple(h)

        if h_tuple in hashes:
            m1 = hashes[h_tuple]
            if m1 != msg:
                log.success(f"  Collision found!")
                log.info(f"    m1={m1.hex()} m2={msg.hex()}")
                return m1, msg
        hashes[h_tuple] = msg

    # Strategy 2: Longer random messages
    log.info("  Trying random messages...")
    from random import Random
    rng = Random(int.from_bytes(iv[:8], 'big'))

    for length in [1, 2, 3, 4, 5]:
        for _ in range(100):
            msg = bytes([rng.randint(0, 255) for _ in range(length)])
            h = gf.hash(msg, iv)
            h_tuple = tuple(h)

            if h_tuple in hashes:
                m1 = hashes[h_tuple]
                if m1 != msg:
                    log.success(f"  Collision found (random)!")
                    return m1, msg
            hashes[h_tuple] = msg

    # Strategy 3: Messages with patterns
    log.info("  Trying patterned messages...")
    for byte_val in range(256):
        for length in [1, 2, 3]:
            msg = bytes([byte_val] * length)
            h = gf.hash(msg, iv)
            h_tuple = tuple(h)

            if h_tuple in hashes:
                m1 = hashes[h_tuple]
                if m1 != msg:
                    log.success(f"  Collision found (pattern)!")
                    return m1, msg
            hashes[h_tuple] = msg

    log.failure("  No collision found")
    return None, None

def main():
    # This challenge runs locally or we can connect
    # Let me assume local for now

    log.info("Testing collision finder locally...")

    import os
    test_iv = os.urandom(16)
    log.info(f"Test IV: {test_iv.hex()}")

    m1, m2 = find_collision(test_iv)

    if m1:
        log.success(f"Found collision!")
        log.info(f"  m1: {m1.hex()}")
        log.info(f"  m2: {m2.hex()}")

        h1 = gf.hash(m1, test_iv)
        h2 = gf.hash(m2, test_iv)
        log.info(f"  h(m1): {h1.hex()}")
        log.info(f"  h(m2): {h2.hex()}")
        log.info(f"  Match: {h1 == h2}")
    else:
        log.failure("Could not find collision")

if __name__ == "__main__":
    context.log_level = 'info'
    main()
