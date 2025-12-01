from fractions import Fraction
from math import isqrt

from Crypto.Util.number import long_to_bytes
from pwn import context, log, remote


context.log_level = "info"


def adjust_diff(diff: int, n: int) -> int:
    """Map a ciphertext difference into (-n/2, n/2) to undo modular reduction."""
    half = n // 2
    if diff > half:
        diff -= n
    if diff < -half:
        diff += n
    return diff


def integer_cuberoot(n: int) -> int:
    """Return the integer cube root using Newton iterations."""
    if n == 0:
        return 0
    x = 1 << ((n.bit_length() + 2) // 3)
    while True:
        y = (2 * x + n // (x * x)) // 3
        if y >= x:
            break
        x = y
    while (x + 1) ** 3 <= n:
        x += 1
    while x**3 > n:
        x -= 1
    return x


def convergents_from_fraction(frac: Fraction, limit: int):
    """Yield convergents of a rational number up to the provided denominator limit."""
    n = frac.numerator
    d = frac.denominator
    if d < 0:
        n, d = -n, -d
    cf = []
    while d:
        a = n // d
        cf.append(a)
        n, d = d, n - a * d
    p_prev, p_curr = 1, cf[0]
    q_prev, q_curr = 0, 1
    yield Fraction(p_curr, q_curr)
    for a in cf[1:]:
        p_prev, p_curr = p_curr, a * p_curr + p_prev
        q_prev, q_curr = q_curr, a * q_curr + q_prev
        if abs(q_curr) > limit:
            break
        yield Fraction(p_curr, q_curr)


def recover_from_pair(delta1: int, delta2: int) -> int:
    """
    Given two differences of ciphertexts (c_i - c_0), recover the plaintext m_0.
    The derivation is explained in writeup.txt; this solves for alpha = (r_1 - r_0)/m_0.
    """
    if delta1 == 0:
        raise ValueError("degenerate delta1")
    frac_delta1 = Fraction(delta1)
    frac_delta2 = Fraction(delta2)
    ratio = frac_delta2 / frac_delta1

    def attempt_with_ratio(s: Fraction):
        if s == 0 or s == 1 or s == -1:
            return None
        t = ratio / s
        a = t - s * s
        b = 3 * (t - s)
        c = 3 * (t - 1)
        if a == 0:
            return None
        discriminant = b * b - 4 * a * c
        if discriminant <= 0:
            return None
        num = discriminant.numerator
        den = discriminant.denominator
        sqrt_num = isqrt(num)
        sqrt_den = isqrt(den)
        if sqrt_num * sqrt_num != num or sqrt_den * sqrt_den != den:
            return None
        sqrt_disc = Fraction(sqrt_num, sqrt_den)
        for sign in (1, -1):
            numerator = -b + sign * sqrt_disc
            denom = 2 * a
            if denom == 0:
                continue
            alpha = numerator / denom
            if alpha == 0 or not (-1 < alpha < 1):
                continue
            m_cubed = frac_delta1 / (alpha * (3 + 3 * alpha + alpha * alpha))
            num = m_cubed.numerator
            den = m_cubed.denominator
            if num % den != 0:
                continue
            value = num // den
            root = integer_cuberoot(value)
            if root**3 == value:
                return root
        return None

    checked = set()
    limit_values = [1 << k for k in range(16, 257, 16)]
    for limit in limit_values:
        s = ratio.limit_denominator(limit)
        if s in checked:
            continue
        checked.add(s)
        result = attempt_with_ratio(s)
        if result is not None:
            return result

    for s in convergents_from_fraction(ratio, 1 << 256):
        if s in checked:
            continue
        checked.add(s)
        result = attempt_with_ratio(s)
        if result is not None:
            return result
    raise ValueError("failed to recover plaintext from pair")


def recover_plaintext(ciphertexts, n: int) -> int:
    base = ciphertexts[0]
    deltas = []
    for c in ciphertexts[1:]:
        diff = adjust_diff(c - base, n)
        if diff != 0:
            deltas.append(diff)
    for i in range(len(deltas)):
        for j in range(i + 1, len(deltas)):
            try:
                return recover_from_pair(deltas[i], deltas[j])
            except ValueError:
                continue
    raise RuntimeError("no valid pair found")


def run_remote():
    r = remote("amt.rs", 37559)
    header = r.recvline().decode()
    n, e = eval(header.split("=")[1].strip())
    log.info(f"N bits: {n.bit_length()}")
    ciphertexts = []
    queries = 6
    for _ in range(queries):
        r.sendlineafter(b"scramble the flag: ", b"0")
        r.recvuntil(b"c = ")
        ciphertexts.append(int(r.recvline().strip()))
    r.close()
    m0 = recover_plaintext(ciphertexts, n)
    flag_bytes = long_to_bytes(m0 >> 256)
    try:
        flag_text = flag_bytes.decode()
    except UnicodeDecodeError:
        flag_text = flag_bytes
    log.success(f"Flag: {flag_text}")


def self_test():
    from Crypto.Util.number import getPrime
    from random import getrandbits

    flag_val = getrandbits(576) << 256
    n = getPrime(1024) * getPrime(1024)
    ciphertexts = []
    for _ in range(6):
        m = flag_val + getrandbits(256)
        ciphertexts.append(pow(m, 3, n))
    recovered = recover_plaintext(ciphertexts, n)
    assert (recovered >> 256) == (flag_val >> 256)
    log.success("Self-test completed")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        self_test()
    else:
        run_remote()
