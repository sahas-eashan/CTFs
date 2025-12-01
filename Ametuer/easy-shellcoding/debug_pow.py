#!/usr/bin/env python3
from pwn import *
import hashlib
import base64
import re

def solve_pow(challenge):
    """Solve hashcash-style PoW challenge"""
    parts = challenge.split('.')
    if len(parts) != 3 or parts[0] != 's':
        return None

    difficulty = int.from_bytes(base64.b64decode(parts[1]), 'big')
    challenge_bytes = base64.b64decode(parts[2])

    log.info(f"Solving PoW: difficulty={difficulty} bits, challenge={challenge_bytes.hex()}")

    nonce = 0
    while True:
        nonce_bytes = nonce.to_bytes((nonce.bit_length() + 7) // 8, 'big') if nonce > 0 else b'\x00'
        test = challenge_bytes + nonce_bytes
        hash_result = hashlib.sha256(test).digest()

        # Count leading zero bits
        zero_bits = 0
        for byte in hash_result:
            if byte == 0:
                zero_bits += 8
            else:
                for i in range(7, -1, -1):
                    if byte & (1 << i):
                        break
                    zero_bits += 1
                break

        if zero_bits >= difficulty:
            solution = base64.b64encode(nonce_bytes).decode()
            log.success(f"PoW solved! Nonce: {nonce}, Solution: {solution}, Hash: {hash_result.hex()}")
            return solution

        nonce += 1

log.info("Connecting...")
io = remote('amt.rs', 57207)

# Receive PoW
data = io.recvuntil(b'solution: ')
print("Received:")
print(data.decode())

# Extract challenge
match = re.search(r's\.[A-Za-z0-9+/=]+\.[A-Za-z0-9+/=]+', data.decode())
if match:
    challenge = match.group(0)
    log.info(f"Challenge: {challenge}")

    solution = solve_pow(challenge)

    log.info(f"Sending solution: {solution}")
    io.sendline(solution.encode())

    # See what happens next
    log.info("Receiving response...")
    try:
        response = io.recv(timeout=5)
        print("\nResponse after PoW:")
        print(response.decode(errors='ignore'))
    except Exception as e:
        log.error(f"Error: {e}")

    # Check if still connected
    if io.connected():
        log.success("Still connected!")
        io.interactive()
    else:
        log.error("Connection closed")
else:
    log.error("Could not extract challenge")

io.close()
