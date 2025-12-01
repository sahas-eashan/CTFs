#!/usr/bin/env python3
"""
Test the pwn.red PoW solver with verification.
"""

import base64

def solve_pwn_red_pow(challenge_str):
    """Solve pwn.red PoW challenge."""
    parts = challenge_str.strip().split('.')
    if len(parts) != 3 or parts[0] != 's':
        raise ValueError(f"Invalid challenge format")

    version = parts[0]
    difficulty_bytes = base64.b64decode(parts[1])
    difficulty = int.from_bytes(difficulty_bytes, byteorder='big')

    challenge_bytes = base64.b64decode(parts[2])
    x = int.from_bytes(challenge_bytes, byteorder='big')

    # Constants
    mod = (1 << 1279) - 1
    exp = 1 << 1277

    # Solve
    for i in range(difficulty):
        x = pow(x, exp, mod)
        x ^= 1

    # Encode
    solution_bytes = x.to_bytes((x.bit_length() + 7) // 8, byteorder='big')
    solution_b64 = base64.b64encode(solution_bytes).decode('ascii')

    return f"{version}.{solution_b64}"


def verify_solution(challenge_str, solution_str):
    """
    Verify a solution by reversing the computation (like the server does).
    """
    # Parse challenge
    challenge_parts = challenge_str.strip().split('.')
    difficulty_bytes = base64.b64decode(challenge_parts[1])
    difficulty = int.from_bytes(difficulty_bytes, byteorder='big')
    challenge_bytes = base64.b64decode(challenge_parts[2])
    challenge_x = int.from_bytes(challenge_bytes, byteorder='big')

    # Parse solution
    solution_parts = solution_str.strip().split('.')
    if len(solution_parts) != 2 or solution_parts[0] != 's':
        return False, "Invalid solution format"

    solution_bytes = base64.b64decode(solution_parts[1])
    y = int.from_bytes(solution_bytes, byteorder='big')

    # Constants
    mod = (1 << 1279) - 1

    # Reverse the computation
    for i in range(difficulty):
        y ^= 1
        y = (y * y) % mod  # Square (reverse of exp)

    # Check if we get back to the challenge (or its negation)
    if y == challenge_x:
        return True, "Solution verified (exact match)"
    elif y == (mod - challenge_x):
        return True, "Solution verified (negation match)"
    else:
        return False, f"Verification failed: got {y}, expected {challenge_x}"


if __name__ == "__main__":
    print("Testing pwn.red PoW solver\n")
    print("=" * 70)

    # Test case 1
    test_challenge = "s.AAAACg==.3wo2Hapx80nWQ0eheMAE/A=="
    print(f"\nTest Challenge: {test_challenge}")

    # Decode to show what it means
    parts = test_challenge.split('.')
    difficulty = int.from_bytes(base64.b64decode(parts[1]), 'big')
    challenge_bytes = base64.b64decode(parts[2])
    print(f"  Difficulty: {difficulty}")
    print(f"  Challenge bytes: {challenge_bytes.hex()}")

    # Solve
    print("\nSolving...")
    solution = solve_pwn_red_pow(test_challenge)
    print(f"Solution: {solution}")

    # Verify
    print("\nVerifying solution...")
    is_valid, message = verify_solution(test_challenge, solution)

    if is_valid:
        print(f"[+] {message}")
        print("\n" + "=" * 70)
        print("SUCCESS! The solver works correctly.")
        print("=" * 70)
    else:
        print(f"[-] {message}")
        print("\n" + "=" * 70)
        print("FAILED! There's an issue with the solver.")
        print("=" * 70)

    print(f"\nFinal solution to send to server:")
    print(solution)
