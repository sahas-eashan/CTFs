#!/usr/bin/env python3
"""
Advanced lattice attack - try different polynomial formulations

Key insight: We have m = F*2^512 + r where F is flag, r is random
And c = m^3 mod n

Let's try expanding this differently and using Howgrave-Graham approach
"""

import sys
from Cryptodome.Util.number import long_to_bytes
from fpylll import LLL, BKZ, IntegerMatrix, GSO


def load_samples(filename="samples.txt"):
    """Load (n, e, c) samples"""
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


def try_univariate_coppersmith(n, c):
    """
    Try univariate approach: assume r is small, solve for F

    m = F*2^512 + r
    m^3 = c + k*n for some k

    Since r < 2^512, we have m ≈ F*2^512
    So (F*2^512)^3 ≈ c (mod n)
    F^3 * 2^1536 ≈ c (mod n)
    F^3 ≈ c * 2^(-1536) (mod n)

    This gives us an approximate cube root
    """
    print("\n  Trying univariate approximation...")

    shift = 2**512

    # Approximate: ignore r, so m ≈ F * shift
    # Then c ≈ (F * shift)^3 mod n
    # c ≈ F^3 * shift^3 mod n

    # Try to take cube root of c / shift^3
    # But this doesn't work directly because of the random r...

    # Alternative: Try small values near the cube root
    approx = pow(c, 1, n)  # c itself
    cbrt_approx = int(approx ** (1/3))

    # Try values around cbrt_approx / shift
    for delta in range(-1000, 1000):
        F_guess = (cbrt_approx // shift) + delta

        if F_guess < 0:
            continue

        # For each F_guess, try to find corresponding r
        # m = F_guess * shift + r
        # m^3 ≡ c (mod n)

        m_base = F_guess * shift

        # Try small r values
        for r in range(0, min(1000, 2**20)):  # Just test small r values
            m = (m_base + r) % n
            c_test = pow(m, 3, n)

            if c_test == c:
                print(f"  ✓ Found solution! F={F_guess}, r={r}")
                return (F_guess, r)

    return None


def try_herrmann_may_bivariate(n, c):
    """
    Herrmann-May style bivariate lattice for small roots

    We want to solve: (x*2^512 + y)^3 - c ≡ 0 (mod n)
    where |x| < X=2^420 and |y| < Y=2^515

    Use lattice with polynomials: f, x*f, y*f, x^2*f, x*y*f, y^2*f, n, ...
    """
    print("\n  Trying Herrmann-May style lattice...")

    X = 2**420  # Flag bound
    Y = 2**515  # Random mask bound
    shift = 2**512

    # Build a larger lattice with polynomial shifts
    # This is a simplified version - full Coppersmith needs more careful construction

    dim = 6
    M = IntegerMatrix(dim, dim)

    # Monomials: [1, x, y, x^2, xy, y^2]
    # Polynomial: (x*shift + y)^3 - c
    # = x^3*shift^3 + 3*x^2*y*shift^2 + 3*x*y^2*shift + y^3 - c

    # Row 0: n (eliminates the modular part)
    M[0, 0] = n
    M[0, 1] = 0
    M[0, 2] = 0
    M[0, 3] = 0
    M[0, 4] = 0
    M[0, 5] = 0

    # Row 1: constant term and x term
    M[1, 0] = -c % n  # constant
    M[1, 1] = X  # x coefficient (scaled)
    M[1, 2] = 0
    M[1, 3] = 0
    M[1, 4] = 0
    M[1, 5] = 0

    # Row 2: y term
    M[2, 0] = 0
    M[2, 1] = 0
    M[2, 2] = Y
    M[2, 3] = 0
    M[2, 4] = 0
    M[2, 5] = 0

    # Row 3: x^2 term
    M[3, 0] = 0
    M[3, 1] = 0
    M[3, 2] = 0
    M[3, 3] = X**2
    M[3, 4] = 0
    M[3, 5] = 0

    # Row 4: xy term
    M[4, 0] = 0
    M[4, 1] = 0
    M[4, 2] = 0
    M[4, 3] = 0
    M[4, 4] = X * Y
    M[4, 5] = 0

    # Row 5: y^2 term
    M[5, 0] = 0
    M[5, 1] = 0
    M[5, 2] = 0
    M[5, 3] = 0
    M[5, 4] = 0
    M[5, 5] = Y**2

    print(f"  Running LLL on {dim}x{dim} matrix...")
    M = LLL.reduction(M)

    # Check first few vectors
    for i in range(min(dim, 3)):
        row = [int(M[i, j]) for j in range(dim)]
        norms = sum(abs(x) for x in row)

        if norms == 0:
            continue

        # Try to extract x, y from the row
        # This is heuristic - proper extraction needs Gröbner bases
        potential_x = abs(row[1]) // X if X != 0 and row[1] != 0 else 0
        potential_y = abs(row[2]) // Y if Y != 0 and row[2] != 0 else 0

        if potential_x > 0 and potential_x < 2**420:
            # Verify
            for r_test in [potential_y, -potential_y]:
                if r_test < 0:
                    continue
                m = (potential_x * shift + r_test) % n
                c_test = pow(m, 3, n)

                if c_test == c:
                    print(f"  ✓ Found solution!")
                    return (potential_x, r_test)

    return None


def main():
    print("="*70)
    print("Advanced Lattice Attack for addition3")
    print("="*70)

    samples = load_samples("samples.txt")
    print(f"\nLoaded {len(samples)} samples")

    # Try first few samples with different methods
    for idx, (n, e, c) in enumerate(samples[:5]):
        print(f"\n{'='*70}")
        print(f"Sample {idx + 1}")
        print(f"{'='*70}")
        print(f"n bits: {n.bit_length()}")
        print(f"c bits: {c.bit_length()}")

        # Method 1: Univariate
        result = try_univariate_coppersmith(n, c)
        if result:
            x, y = result
            flag_bytes = long_to_bytes(int(x))
            print(f"\n{'='*70}")
            print(f"SUCCESS via univariate!")
            print(f"Flag: {flag_bytes}")
            print(f"{'='*70}")
            return

        # Method 2: Bivariate lattice
        result = try_herrmann_may_bivariate(n, c)
        if result:
            x, y = result
            flag_bytes = long_to_bytes(int(x))
            print(f"\n{'='*70}")
            print(f"SUCCESS via bivariate lattice!")
            print(f"Flag: {flag_bytes}")
            print(f"{'='*70}")
            return

    print(f"\n{'='*70}")
    print("No solution found.")
    print("This challenge likely needs full Coppersmith (SageMath) or a different approach.")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
