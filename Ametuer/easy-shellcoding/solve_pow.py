#!/usr/bin/env python3
import hashlib
import base64
import sys

def solve_pow(challenge):
    """
    Solve the proof-of-work challenge.
    Format: s.difficulty.challenge
    We need to find a nonce such that:
    sha256(challenge + nonce) starts with 'difficulty' number of zero bits
    """
    parts = challenge.split('.')
    if len(parts) != 3 or parts[0] != 's':
        print(f"Invalid challenge format: {challenge}")
        return None

    difficulty_b64 = parts[1]
    challenge_b64 = parts[2]

    # Decode difficulty (number of zero bits required)
    difficulty = int.from_bytes(base64.b64decode(difficulty_b64), 'big')
    challenge_bytes = base64.b64decode(challenge_b64)

    print(f"[*] Difficulty: {difficulty} zero bits")
    print(f"[*] Challenge: {challenge_bytes.hex()}")

    # Brute force to find nonce
    nonce = 0
    while True:
        nonce_bytes = nonce.to_bytes((nonce.bit_length() + 7) // 8, 'big') if nonce > 0 else b'\x00'
        test = challenge_bytes + nonce_bytes
        hash_result = hashlib.sha256(test).digest()

        # Check if hash has required zero bits
        zero_bits = 0
        for byte in hash_result:
            if byte == 0:
                zero_bits += 8
            else:
                # Count leading zeros in this byte
                for i in range(7, -1, -1):
                    if byte & (1 << i):
                        break
                    zero_bits += 1
                break

        if zero_bits >= difficulty:
            solution = base64.b64encode(nonce_bytes).decode()
            print(f"[+] Found solution: {solution}")
            print(f"[+] Nonce: {nonce} ({nonce_bytes.hex()})")
            print(f"[+] Hash: {hash_result.hex()}")
            return solution

        nonce += 1
        if nonce % 100000 == 0:
            print(f"[*] Tried {nonce} nonces...")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        challenge = sys.argv[1]
    else:
        challenge = input("Enter challenge: ").strip()

    solution = solve_pow(challenge)
    if solution:
        print(f"\nSolution: {solution}")
