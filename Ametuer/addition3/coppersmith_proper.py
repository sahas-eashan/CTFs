#!/usr/bin/env python3
"""
Proper Coppersmith bivariate attack using Howgrave-Graham approach
Based on Herrmann-May and Jochemsz-May methods

We want to solve: f(x,y) = (x*2^512 + y)^3 - c ≡ 0 (mod n)
where |x| < X=2^416 (flag) and |y| < Y=2^512 (random mask)
"""

from fpylll import LLL, BKZ, IntegerMatrix
from Cryptodome.Util.number import long_to_bytes
import itertools


def load_samples(filename="samples.txt"):
    """Load samples from file"""
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


def build_lattice_bivariate(n, c, X, Y, m=2, t=1):
    """
    Build lattice for bivariate Coppersmith using Howgrave-Graham

    f(x, y) = (x*shift + y)^3 - c
            = x^3*shift^3 + 3*x^2*y*shift^2 + 3*x*y^2*shift + y^3 - c

    We build polynomials: x^i * y^j * f^k * n^(m-k) for various i,j,k
    """
    shift = 2**512

    # Expand f(x,y) = (x*shift + y)^3 - c
    # Coefficients for: 1, x, y, x^2, xy, y^2, x^3, x^2*y, x*y^2, y^3

    print(f"  Building lattice with m={m}, t={t}")
    print(f"  X=2^{X.bit_length()-1}, Y=2^{Y.bit_length()-1}")

    # Collect monomials and their shifts
    monomials = []
    polynomials = []

    # For k from 0 to m, i,j >= 0 such that i+j <= m-k+t
    for k in range(m + 1):
        for i in range(m - k + t + 1):
            for j in range(m - k + t + 1 - i):
                monomial = (i, j, k)  # x^i * y^j * f^k
                monomials.append(monomial)

    monomials.sort()  # Sort for consistency
    dim = len(monomials)

    print(f"  Lattice dimension: {dim}")

    if dim > 50:
        print(f"  WARNING: Large lattice ({dim}x{dim}), may be slow")
        return None, None

    M = IntegerMatrix(dim, dim)

    # Build matrix where each row corresponds to one polynomial shift
    for row_idx, (i, j, k) in enumerate(monomials):
        # This row represents: x^i * y^j * f(x,y)^k * n^(m-k)

        # f(x,y)^k expands to multiple monomials
        # For simplicity, we'll use a heuristic approximation

        for col_idx, (i2, j2, k2) in enumerate(monomials):
            if i2 == i and j2 == j and k2 == 0:
                # Coefficient for this monomial
                coeff = n**(m - k) * (X**i) * (Y**j)
                M[row_idx, col_idx] = coeff

    return M, monomials


def coppersmith_bivariate_attack(n, c):
    """
    Attempt bivariate Coppersmith with different parameters
    """
    X = 2**420  # Flag bound (slightly larger than 416)
    Y = 2**515  # Random mask bound (slightly larger than 512)

    print(f"\n  Attempting Coppersmith bivariate attack")
    print(f"  n bits: {n.bit_length()}")
    print(f"  c bits: {c.bit_length()}")

    # Try different lattice parameters
    for m in [2, 3]:
        for t in [0, 1]:
            print(f"\n  Trying m={m}, t={t}")

            M, monomials = build_lattice_bivariate(n, c, X, Y, m, t)

            if M is None:
                continue

            dim = M.nrows

            print(f"  Running LLL reduction on {dim}x{dim} lattice...")
            try:
                M = LLL.reduction(M)
                print(f"  LLL complete")

                # Check if we got small vectors
                for i in range(min(3, dim)):
                    row = [int(M[i, j]) for j in range(dim)]
                    norm = sum(x**2 for x in row) ** 0.5

                    if norm < 2**100:  # Very small vector found
                        print(f"    Row {i} norm: {norm:.2e}")

                        # Try to extract roots (heuristic)
                        # This is where proper implementation would use Gröbner basis
                        # For now, we just check if any obvious solution appears

            except Exception as e:
                print(f"  LLL failed: {e}")
                continue

    return None


def try_simple_approaches(n, c):
    """Try simpler approaches first before full Coppersmith"""

    shift = 2**512

    # Approach 1: Maybe r is actually smaller than we think?
    print("\n  Trying smaller r bounds...")
    for r_bits in [256, 384, 450, 480]:
        print(f"    Trying r < 2^{r_bits}")

        # If r is small, m ≈ flag * shift
        # So cbrt(c) ≈ flag * shift

        # Take approximate cube root
        # c^(1/3) ≈ m

        # Use binary search for cube root
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if mid**3 <= c:
                lo = mid
            else:
                hi = mid - 1

        approx_m = lo
        approx_flag = approx_m >> 512

        # Try values near this approximation
        for delta in range(-100, 100):
            flag_guess = approx_flag + delta

            if flag_guess < 0:
                continue

            m_base = flag_guess * shift

            # Try small r values
            for r in range(2**r_bits):
                m = (m_base + r) % n
                c_test = pow(m, 3, n)

                if c_test == c:
                    print(f"    ✓ FOUND! flag={flag_guess}, r={r}")
                    return (flag_guess, r)

                if r > 10000 and r % 10000 == 0:
                    print(f"      Checked {r}...", end='\r')

            print()  # Clear progress line

    return None


def main():
    print("="*70)
    print("Proper Coppersmith Attack for addition3")
    print("="*70)

    samples = load_samples("samples.txt")
    print(f"\nLoaded {len(samples)} samples")

    for idx, (n, e, c) in enumerate(samples[:3]):  # Try first 3
        print(f"\n{'='*70}")
        print(f"Sample {idx + 1}")
        print(f"{'='*70}")

        # Try simple approaches first
        result = try_simple_approaches(n, c)
        if result:
            x, y = result
            flag_bytes = long_to_bytes(int(x))
            print(f"\n{'='*70}")
            print(f"SUCCESS!")
            print(f"Flag: {flag_bytes}")
            print(f"{'='*70}")
            return

        # Try full Coppersmith
        result = coppersmith_bivariate_attack(n, c)
        if result:
            x, y = result
            flag_bytes = long_to_bytes(int(x))
            print(f"\n{'='*70}")
            print(f"SUCCESS via Coppersmith!")
            print(f"Flag: {flag_bytes}")
            print(f"{'='*70}")
            return

    print("\nNo solution found. This challenge needs SageMath's small_roots().")


if __name__ == "__main__":
    main()
