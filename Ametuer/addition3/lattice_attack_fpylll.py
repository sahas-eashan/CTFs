#!/usr/bin/env python3
"""
Lattice attack on addition3 using fpylll
Run in WSL: wsl python3 lattice_attack_fpylll.py

The challenge: m = (flag << 512) + r where flag ~416 bits, r ~512 bits
We have: c = m^3 mod n

This is a bivariate small roots problem:
f(x, y) = (x*2^512 + y)^3 - c ≡ 0 (mod n)

We need to find small x (flag) and y (random mask r).
"""

import sys

try:
    from fpylll import LLL, BKZ, IntegerMatrix
    from Cryptodome.Util.number import long_to_bytes
except ImportError:
    print("Missing dependencies. Install with:")
    print("  pip3 install fpylll pycryptodomex")
    sys.exit(1)


def load_samples(filename="samples.txt"):
    """Load (n, e, c) samples from file"""
    samples = []
    with open(filename) as f:
        lines = f.read().strip().split('\n')

    n, e, c = None, None, None
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        if line.startswith('n = '):
            if n is not None and e is not None and c is not None:
                samples.append((n, e, c))
            n = int(line.split('=')[1].strip())
            e, c = None, None
        elif line.startswith('e = '):
            e = int(line.split('=')[1].strip())
        elif line.startswith('c = '):
            c = int(line.split('=')[1].strip())

    if n is not None and e is not None and c is not None:
        samples.append((n, e, c))

    return samples


def small_roots_bivariate_simple(n, c, X, Y):
    """
    Attempt simple lattice attack for (x*2^512 + y)^3 - c ≡ 0 (mod n)
    where |x| < X (flag) and |y| < Y (random mask)

    This uses a simplified lattice construction.
    """
    print(f"  Trying bounds: X=2^{X.bit_length()}, Y=2^{Y.bit_length()}")

    # Expand (x*2^512 + y)^3
    # = x^3 * 2^1536 + 3*x^2*y*2^1024 + 3*x*y^2*2^512 + y^3 - c

    shift = 2**512

    # Build lattice for the polynomial
    # We want to find (x, y) such that:
    # x^3 * shift^3 + 3*x^2*y*shift^2 + 3*x*y^2*shift + y^3 ≡ c (mod n)

    # Use a simple 2x2 lattice approach
    # Row 1: [n, 0]
    # Row 2: [c, X*Y]

    # This is too simple - let's try a 3x3 lattice
    dim = 3
    M = IntegerMatrix(dim, dim)

    # Scale factors
    scale_x = X
    scale_y = Y

    M[0, 0] = n
    M[0, 1] = 0
    M[0, 2] = 0

    M[1, 0] = c
    M[1, 1] = scale_x
    M[1, 2] = 0

    M[2, 0] = 0
    M[2, 1] = 0
    M[2, 2] = scale_y

    print(f"  Running LLL on {dim}x{dim} matrix...")
    M = LLL.reduction(M)

    print(f"  Shortest vector: {M[0]}")

    # Check if we got something useful
    for i in range(min(dim, 3)):
        row = [M[i, j] for j in range(dim)]
        print(f"    Row {i}: {row[:3]}")

        # Try to extract potential x, y values
        if abs(row[1]) < X and abs(row[2]) < Y:
            x_cand = abs(row[1]) // scale_x if scale_x != 0 else 0
            y_cand = abs(row[2]) // scale_y if scale_y != 0 else 0

            # Verify
            m = (x_cand * shift + y_cand) % n
            c_check = pow(m, 3, n)

            if c_check == c:
                print(f"  ✓ Found solution!")
                return (x_cand, y_cand)

    return None


def coppersmith_bivariate_attempt(n, c):
    """
    Try to solve (x*2^512 + y)^3 ≡ c (mod n)
    using lattice-based small roots finding
    """
    # Flag is 52 bytes = 416 bits
    # Random mask is 512 bits

    # Try different bounds
    bounds = [
        (2**420, 2**515),   # Slightly larger than expected
        (2**416, 2**512),   # Exact expected sizes
        (2**410, 2**510),   # Slightly smaller
    ]

    for X, Y in bounds:
        print(f"\nAttempting with X=2^{X.bit_length()-1}, Y=2^{Y.bit_length()-1}")
        result = small_roots_bivariate_simple(n, c, X, Y)
        if result:
            return result

    return None


def main():
    print("="*70)
    print("addition3 Lattice Attack using fpylll")
    print("="*70)

    samples = load_samples("samples.txt")
    print(f"\nLoaded {len(samples)} samples")

    if not samples:
        print("No samples found! Run collect_samples.py first.")
        return

    # Try each sample
    for idx, (n, e, c) in enumerate(samples[:10]):  # Try first 10
        print(f"\n{'='*70}")
        print(f"Sample {idx + 1}/{len(samples)}")
        print(f"{'='*70}")
        print(f"n bits: {n.bit_length()}")
        print(f"c bits: {c.bit_length()}")

        result = coppersmith_bivariate_attempt(n, c)

        if result:
            x, y = result
            flag_int = x
            flag_bytes = long_to_bytes(int(flag_int))

            print(f"\n{'='*70}")
            print(f"SUCCESS! Found flag:")
            print(f"{'='*70}")
            print(f"Flag (int): {flag_int}")
            print(f"Flag (bytes): {flag_bytes}")
            print(f"{'='*70}")
            return

        print(f"  Sample {idx + 1} failed, trying next...")

    print(f"\n{'='*70}")
    print("No solution found in available samples.")
    print("This challenge likely needs more advanced Coppersmith implementation")
    print("or SageMath with proper polynomial small_roots() method.")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
