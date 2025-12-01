#!/usr/bin/env python3
"""
Correct pwn.red proof-of-work solver implementation.

The pwn.red PoW system uses modular exponentiation, NOT SHA256!

Algorithm:
- Modulus: 2^1279 - 1
- Exponent: 2^1277
- To solve: Start with challenge x, repeat difficulty times: x = (x^exp mod mod) XOR 1
- Solution format: s.BASE64(solution_bytes)
"""

import base64
import sys

def solve_pow(challenge_str):
    """
    Solve pwn.red proof-of-work challenge.

    Challenge format: s.BASE64(difficulty).BASE64(challenge)
    Solution format: s.BASE64(solution)

    Args:
        challenge_str: The challenge string (e.g., "s.AAAACg==.3wo2Hapx80nWQ0eheMAE/A==")

    Returns:
        Solution string in format "s.BASE64(solution)"
    """
    parts = challenge_str.strip().split('.')
    if len(parts) != 3 or parts[0] != 's':
        raise ValueError(f"Invalid challenge format: {challenge_str}")

    version = parts[0]
    difficulty_b64 = parts[1]
    challenge_b64 = parts[2]

    # Decode difficulty and challenge
    difficulty_bytes = base64.b64decode(difficulty_b64)
    difficulty = int.from_bytes(difficulty_bytes, byteorder='big')

    challenge_bytes = base64.b64decode(challenge_b64)
    x = int.from_bytes(challenge_bytes, byteorder='big')

    print(f"[*] Challenge: {challenge_str}")
    print(f"[*] Difficulty: {difficulty} iterations")
    print(f"[*] Challenge value: {x}")

    # Constants from redpwn/pow
    # mod = 2^1279 - 1
    mod = (1 << 1279) - 1
    # exp = 2^1277
    exp = 1 << 1277

    # Solve: perform the computation
    # Start with x, repeat difficulty times: x = (x^exp mod mod) XOR 1
    for i in range(difficulty):
        x = pow(x, exp, mod)  # Modular exponentiation
        x ^= 1  # XOR with 1
        if (i + 1) % 1000 == 0:
            print(f"[*] Progress: {i + 1}/{difficulty} iterations")

    # Convert solution to bytes
    # Determine byte length needed
    solution_bytes = x.to_bytes((x.bit_length() + 7) // 8, byteorder='big')

    # Encode solution
    solution_b64 = base64.b64encode(solution_bytes).decode('ascii')
    solution = f"{version}.{solution_b64}"

    print(f"[+] Solution: {solution}")
    print(f"[+] Solution value: {x}")

    return solution


if __name__ == "__main__":
    if len(sys.argv) > 1:
        challenge = sys.argv[1]
    else:
        challenge = input("Enter challenge: ").strip()

    try:
        solution = solve_pow(challenge)
        print(f"\n=== SOLUTION ===")
        print(solution)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
