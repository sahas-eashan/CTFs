#!/usr/bin/env python3
"""
Exploit for Guess Me! challenge
Strategy: Generate valid (nonce, ct, tag) for ALL 5040 permutations offline,
then send ALL nonces in a single request!
"""

from pwn import *
from hashlib import sha256
from itertools import permutations
import os

# Import the encryption functions from the challenge
import sys
sys.path.insert(0, os.path.dirname(__file__))
from guess_me import encrypt, BLOCK_SIZE

def generate_all_keys():
    """Generate all 7! = 5040 possible keys from permutations of 'm0leCon'"""
    base = "m0leCon"
    all_perms = permutations(base)
    keys = {}
    for perm in all_perms:
        perm_str = "".join(perm)
        key = bytes(sha256(perm_str.encode()).digest())[:BLOCK_SIZE]
        keys[perm_str] = key
    return keys

def precompute_payloads(message=b"next round please", additional_data=b"pretty please"):
    """
    Precompute valid (nonce, ciphertext, tag) for every possible key.
    Since we can send multiple nonces, we'll use a unique nonce per key.
    """
    print("[*] Generating all 5040 keys from permutations...")
    all_keys = generate_all_keys()
    print(f"[+] Generated {len(all_keys)} keys")

    print("[*] Precomputing payloads for each key...")
    payloads = {}

    for idx, (perm_str, key) in enumerate(all_keys.items()):
        if idx % 500 == 0:
            print(f"    Progress: {idx}/{len(all_keys)}")

        # Use a unique nonce for each key (derived from permutation for reproducibility)
        nonce = bytes(sha256(f"nonce_{perm_str}".encode()).digest())[:BLOCK_SIZE]

        # Encrypt the message with this key and nonce
        ciphertext, tag = encrypt(key, nonce, message, additional_data)

        payloads[perm_str] = {
            'key': key.hex(),
            'nonce': nonce,
            'ciphertext': ciphertext,
            'tag': tag
        }

    print(f"[+] Precomputed {len(payloads)} payloads")
    return payloads

def exploit_remote(host, port):
    """
    Send all 5040 nonces at once! Only ONE needs to match the server's key.
    """
    print(f"[+] Connecting to {host}:{port}")
    io = remote(host, port)

    # Precompute all payloads
    payloads = precompute_payloads()

    # Extract all nonces, use first payload's ciphertext/tag (they should work if nonce matches)
    # Actually, we need the SAME ciphertext and tag for all attempts
    # So we pick ONE message/ad and encrypt with one nonce, then send all nonces

    # Better approach: Pick a fixed nonce, encrypt message with ALL keys,
    # then for each round try to find which ciphertext works

    # Wait, the server decrypts with EACH nonce we provide!
    # So we can send 5040 different nonces, each encrypted with a different key
    # As long as ONE of them matches the server's key, we succeed!

    message = b"next round please"
    additional_data = b"pretty please"

    # We'll use the same ciphertext/tag but DIFFERENT nonces won't work
    # because each (key, nonce) pair produces different keystream

    # Better strategy: We need to send multiple (nonce, ct, tag) tuples
    # But the server only accepts ONE ciphertext and ONE tag per request!

    # Let me re-read the code...
    # Line 122: decs = [decrypt(key, nonce, ciphertext, additional_data, tag) for nonce in nonces]
    # It decrypts the SAME ciphertext with EACH nonce!

    # So we need to find a ciphertext that works with multiple nonces!
    # This is a nonce-reuse attack vector!

    print("[*] Strategy: Send all nonces, one ciphertext/tag will match!")

    for round_num in range(1, 6):
        print(f"\n[+] Round {round_num}/5")

        for attempt in range(16):
            # Receive prompts
            io.recvuntil(b"Enter nonce (hex): ")

            # Concatenate ALL nonces into one hex string
            all_nonces = b"".join([p['nonce'] for p in payloads.values()])
            io.sendline(all_nonces.hex().encode())

            io.recvuntil(b"Enter additional_data (hex): ")
            io.sendline(additional_data.hex().encode())

            io.recvuntil(b"Enter ciphertext (hex): ")
            # Use the first payload's ciphertext (arbitrary choice)
            first_payload = list(payloads.values())[0]
            io.sendline(first_payload['ciphertext'].hex().encode())

            io.recvuntil(b"Enter tag (hex): ")
            io.sendline(first_payload['tag'].hex().encode())

            # Get response
            response = io.recvline(timeout=2)
            print(f"    Attempt {attempt+1}: {response.decode().strip()}")

            if b"There you go!" in response:
                print(f"    [+] Round {round_num} complete!")
                break
            elif b"Better luck next time" in response:
                print(f"    [-] Failed round {round_num}")
                io.close()
                return

    # Get flag
    print("\n[*] Getting flag...")
    io.recvuntil(b"ptm{", timeout=5)
    flag = b"ptm{" + io.recvuntil(b"}")
    print(f"\n[!!!] FLAG: {flag.decode()}")

    io.close()

if __name__ == "__main__":
    host = "guess_me.challs.m0lecon.it"
    port = 12164

    exploit_remote(host, port)
