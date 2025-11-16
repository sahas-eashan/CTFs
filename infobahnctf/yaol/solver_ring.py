#!/usr/bin/env python3
"""
Solver skeleton for Kyoko_Ring discrete log / secret recovery.

You must paste the printed matrices g and g_secret from the challenge instance
(and the AES ciphertext hex). The script attempts to recover the 580-bit secret
using valuation / linear-term extraction heuristics in the mixed (p,q)-adic ring.

NOTE: Without the original challenge output (the two matrices + ciphertext),
this script cannot recover the real flag.
"""
from __future__ import annotations
import re, sys, math, hashlib
from typing import List, Tuple, Optional
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

Matrix = List[List[int]]


class KyokoRingElement:
    def __init__(self, p: int, q: int, data: Matrix):
        self.p = p
        self.q = q
        self.data = data

    def __mul__(self, other: "KyokoRingElement") -> "KyokoRingElement":
        p, q = self.p, self.q
        out = [[0] * 3 for _ in range(3)]
        for i in range(3):
            for k in range(3):
                acc = 0
                for j in range(3):
                    acc += self.data[i][j] * other.data[j][k]
                # modulus per position
                mod = (p ** (i + 1)) * (q ** (k + 1))
                out[i][k] = acc % mod
        return KyokoRingElement(p, q, out)

    def __pow__(self, e: int) -> "KyokoRingElement":
        assert e >= 0
        p, q = self.p, self.q
        # identity
        out = KyokoRingElement(
            p, q, [[1 if i == j else 0 for j in range(3)] for i in range(3)]
        )
        base = KyokoRingElement(p, q, [row[:] for row in self.data])
        while e:
            if e & 1:
                out = out * base
            base = base * base
            e >>= 1
        return out

    def __repr__(self):
        return str(self.data)


MATRIX_RE = re.compile(r"\[(?:\s*\[.*?\]\s*,?){3}\]")


def parse_matrix(text: str) -> Matrix:
    # Expect Python-style nested list. Use eval safely by filtering digits & brackets & commas.
    if not MATRIX_RE.search(text):
        raise ValueError("Matrix text not found")
    safe = re.sub(r"[^0-9,\[\]]", "", text)
    mat = eval(safe)  # list of lists of ints
    if not (
        isinstance(mat, list)
        and all(isinstance(r, list) and len(r) == 3 for r in mat)
        and len(mat) == 3
    ):
        raise ValueError("Unexpected matrix shape")
    return mat


def egcd(a: int, b: int) -> Tuple[int, int, int]:
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)


def modinv(a: int, m: int) -> int:
    a %= m
    g, x, y = egcd(a, m)
    if g != 1:
        raise ValueError("no inverse")
    return x % m


def crt_pair(a1: int, m1: int, a2: int, m2: int) -> Tuple[int, int]:
    # Solve x ≡ a1 (mod m1), x ≡ a2 (mod m2)
    g, s, t = egcd(m1, m2)
    if (a2 - a1) % g != 0:
        raise ValueError("CRT incompatible")
    lcm = (m1 // g) * m2
    k = ((a2 - a1) // g) * s % (m2 // g)
    x = (a1 + m1 * k) % lcm
    return x, lcm


def infer_p_q_from_mats(g: Matrix, h: Matrix) -> Tuple[int, int]:
    # Positions with minimal p-power: (1,0), (2,1)
    p_gcd = 0
    for i, j in [(1, 0), (2, 1)]:
        p_gcd = math.gcd(p_gcd, abs(g[i][j]))
        p_gcd = math.gcd(p_gcd, abs(h[i][j]))
    # Positions with minimal q-power: (0,1), (1,2)
    q_gcd = 0
    for i, j in [(0, 1), (1, 2)]:
        q_gcd = math.gcd(q_gcd, abs(g[i][j]))
        q_gcd = math.gcd(q_gcd, abs(h[i][j]))
    # With overwhelming probability, these equal p and q.
    return p_gcd, q_gcd


def p_adic_log_series(u: int, p: int, r: int) -> int:
    # Compute log(u) modulo p^r where u ≡ 1 (mod p)
    mod = p**r
    t = (u - 1) % mod
    # series up to r terms; for r<=3, use t - t^2/2 + t^3/3
    res = t % mod
    if r >= 2:
        res = (res - (t * t // 2) % mod) % mod
    if r >= 3:
        # compute t^3/3 using integer division; t is divisible by p
        res = (res + (t * t % mod * t % mod) * modinv(3, mod)) % mod
    return res


def recover_e_mod_p2_q2(p: int, q: int, g: Matrix, h: Matrix) -> Tuple[int, int]:
    # Use diagonal (2,2) for depth r=3 (p^3, q^3) reductions
    a = g[2][2]
    b = h[2][2]
    # p-adic side
    r = 3
    mod_p = p**r
    up = pow(a % mod_p, (p - 1), mod_p)
    vp = pow(b % mod_p, (p - 1), mod_p)
    Lp_u = p_adic_log_series(up, p, r)
    Lp_v = p_adic_log_series(vp, p, r)
    # divide by p to get modulo p^{r-1}
    Lp_u_div = (Lp_u // p) % (p ** (r - 1))
    Lp_v_div = (Lp_v // p) % (p ** (r - 1))
    if Lp_u_div == 0:
        raise ValueError("Degenerate p-adic log: base not suitable")
    e_mod_p2 = (Lp_v_div * modinv(Lp_u_div, p ** (r - 1))) % (p ** (r - 1))
    # q-adic side
    mod_q = q**r
    uq = pow(a % mod_q, (q - 1), mod_q)
    vq = pow(b % mod_q, (q - 1), mod_q)
    Lq_u = p_adic_log_series(uq, q, r)
    Lq_v = p_adic_log_series(vq, q, r)
    Lq_u_div = (Lq_u // q) % (q ** (r - 1))
    Lq_v_div = (Lq_v // q) % (q ** (r - 1))
    if Lq_u_div == 0:
        raise ValueError("Degenerate q-adic log: base not suitable")
    e_mod_q2 = (Lq_v_div * modinv(Lq_u_div, q ** (r - 1))) % (q ** (r - 1))
    return e_mod_p2, e_mod_q2


def recover_secret(p: int, q: int, g: Matrix, gexp: Matrix) -> Tuple[int, int, int]:
    """Return (e_p2, e_q2, e_mod) where e_mod is CRT of e modulo p^2 and q^2.
    This is partial information; the full secret cannot be determined without
    additional structure or more output from the instance.
    """
    e_p2, e_q2 = recover_e_mod_p2_q2(p, q, g, gexp)
    e_crt, mod = crt_pair(e_p2, p**2, e_q2, q**2)
    return e_p2, e_q2, e_crt


# -------- Linear lifting on off-diagonal entries ---------


def entry_modulus(i: int, j: int, p: int, q: int) -> int:
    return (p ** (i + 1)) * (q ** (j + 1))


def is_linear_entry(
    G: KyokoRingElement, i: int, j: int, trials: int = 6
) -> Optional[Tuple[int, int, int]]:
    """Check if f(e) = (G**e)[i][j] is affine linear mod M for e in [0..trials].
    Returns (a, b, M) such that f(e) ≡ a*e + b (mod M), else None.
    """
    p, q = G.p, G.q
    M = entry_modulus(i, j, p, q)
    I = KyokoRingElement(
        p, q, [[1 if r == c else 0 for c in range(3)] for r in range(3)]
    )
    vals = []
    P = I
    for e in range(trials + 1):
        if e == 0:
            vals.append(P.data[i][j] % M)
        else:
            P = P * G
            vals.append(P.data[i][j] % M)
    # Fit affine: a = f(1)-f(0), b=f(0)
    a = (vals[1] - vals[0]) % M
    b = vals[0]
    ok = True
    for e in range(trials + 1):
        if (a * e + b) % M != vals[e]:
            ok = False
            break
    if ok:
        return a, b, M
    return None


def solve_linear_congruences(
    G: KyokoRingElement, H: KyokoRingElement
) -> Tuple[int, int]:
    """Try to recover exponent E by finding multiple linear entries and combining via CRT.
    Returns (E, modulus) meaning E ≡ secret (mod modulus). May equal the full secret if modulus is large.
    """
    congruences: List[Tuple[int, int]] = []
    for i in range(3):
        for j in range(3):
            probe = is_linear_entry(G, i, j, 6)
            if probe is None:
                continue
            a, b, M = probe
            # Need to solve a*E ≡ (H_ij - b) (mod M)
            rhs = (H.data[i][j] - b) % M
            d = math.gcd(a, M)
            if rhs % d != 0:
                continue
            a_ = a // d
            M_ = M // d
            rhs_ = (rhs // d) % M_
            try:
                inv = modinv(a_, M_)
            except Exception:
                continue
            e0 = (rhs_ * inv) % M_
            # record congruence E ≡ e0 (mod M_)
            congruences.append((e0, M_))
    if not congruences:
        return 0, 1
    # Combine via CRT
    x, m = congruences[0]
    for a1, m1 in congruences[1:]:
        x, m = crt_pair(x, m, a1, m1)
    return x, m


def full_recover_secret(p: int, q: int, g: Matrix, h: Matrix) -> Tuple[int, int]:
    """Attempt to fully recover secret by linear lifting on multiple bases.
    Tries bases G = g^t for t in {1, p-1, q-1, (p-1)(q-1)} and combines CRT info.
    Returns (E, modulus). If modulus is large enough (>= 2^580), E is unique.
    """
    base = KyokoRingElement(p, q, [row[:] for row in g])
    target = KyokoRingElement(p, q, [row[:] for row in h])
    ts = [1, p - 1, q - 1, (p - 1) * (q - 1), p, q, p * (q - 1), q * (p - 1)]
    x = None
    m = None
    for t in ts:
        Gt = base**t
        Ht = target**t
        e_t, mod_t = solve_linear_congruences(Gt, Ht)
        if mod_t == 1:
            continue
        if x is None:
            x, m = e_t, mod_t
        else:
            try:
                x, m = crt_pair(x, m, e_t, mod_t)
            except Exception:
                # skip incompatible
                pass
    if x is None:
        return 0, 1
    return x, m


# ---------------- Quadratic fitting and Hensel lifting ----------------
def inv2_mod(m: int) -> int:
    return modinv(2, m)


def legendre_symbol(a: int, p: int) -> int:
    return pow(a % p, (p - 1) // 2, p)


def tonelli_shanks(n: int, p: int) -> Optional[int]:
    n %= p
    if n == 0:
        return 0
    if p == 2:
        return n
    ls = legendre_symbol(n, p)
    if ls != 1:
        return None
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)
    # factor p-1 = q*2^s
    qv = p - 1
    s = 0
    while qv % 2 == 0:
        qv //= 2
        s += 1
    # find z non-residue
    z = 2
    while legendre_symbol(z, p) != p - 1:
        z += 1
    c = pow(z, qv, p)
    x = pow(n, (qv + 1) // 2, p)
    t = pow(n, qv, p)
    m = s
    while t != 1:
        i = 1
        t2i = (t * t) % p
        while i < m and t2i != 1:
            t2i = (t2i * t2i) % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        x = (x * b) % p
        t = (t * b * b) % p
        c = (b * b) % p
        m = i
    return x


def hensel_lift_simple_root(A: int, B: int, C: int, p: int, r: int, x0: int) -> int:
    # Lift solution x0 mod p to mod p^r for f(x)=A x^2 + B x + C
    x = x0 % p
    mod = p
    for k in range(1, r):
        mod *= p
        fx = (A * x * x + B * x + C) % mod
        dfx = (2 * A * x + B) % p
        inv = modinv(dfx, p)
        # compute t such that x' = x - t with t ≡ fx/dfx mod p^{k}
        t = (fx // (mod // p)) * inv % p
        x = (x - t * (mod // p)) % mod
    return x


def solve_quadratic_prime_power(A: int, B: int, C: int, p: int, r: int) -> List[int]:
    # Solve A x^2 + B x + C ≡ 0 (mod p^r)
    if r <= 0:
        return []
    Ap = A % p
    Bp = B % p
    Cp = C % p
    if Ap == 0:
        if Bp % p == 0:
            return []
        x0 = (-Cp * modinv(Bp, p)) % p
        # linear lift
        x = x0
        mod = p
        for k in range(1, r):
            mod *= p
            val = (A * x * x + B * x + C) % mod
            t = ((-val // (mod // p)) * modinv(B % p, p)) % p
            x = (x + t * (mod // p)) % mod
        return [x]
    # Quadratic case
    D = (Bp * Bp - 4 * Ap * Cp) % p
    sqrtD = tonelli_shanks(D, p)
    if sqrtD is None:
        return []
    inv2A = modinv((2 * Ap) % p, p)
    roots_p = [((-Bp + sqrtD) * inv2A) % p, ((-Bp - sqrtD) * inv2A) % p]
    res = []
    for x0 in roots_p:
        dfx = (2 * Ap * x0 + Bp) % p
        if dfx == 0:
            continue
        res.append(hensel_lift_simple_root(A, B, C, p, r, x0))
    return res


def fit_quadratic_standard(
    G: KyokoRingElement, i: int, j: int
) -> Optional[Tuple[int, int, int, int]]:
    # Fit f(e) = a2 e^2 + a1 e + a0 mod M using e=0,1,2; verify e=3
    p, q = G.p, G.q
    M = entry_modulus(i, j, p, q)
    I = KyokoRingElement(
        p, q, [[1 if r == c else 0 for c in range(3)] for r in range(3)]
    )
    vals = []
    P = I
    for e in range(4):
        if e == 0:
            vals.append(P.data[i][j] % M)
        else:
            P = P * G
            vals.append(P.data[i][j] % M)
    v0, v1, v2, v3 = vals
    a0 = v0 % M
    inv2 = inv2_mod(M)
    a2 = ((v2 - 2 * v1 + v0) * inv2) % M
    a1 = (v1 - v0 - a2) % M
    # verify at e=3
    pred3 = (a2 * 9 + a1 * 3 + a0) % M
    if pred3 != v3 % M:
        return None
    return a0, a1, a2, M


def quadratic_lift_recover(p: int, q: int, g: Matrix, h: Matrix) -> Tuple[int, int]:
    base = KyokoRingElement(p, q, [row[:] for row in g])
    target = KyokoRingElement(p, q, [row[:] for row in h])
    best_x = None
    best_m = 1
    for i in range(3):
        for j in range(3):
            fit = fit_quadratic_standard(base, i, j)
            if not fit:
                continue
            a0, a1, a2, M = fit
            y = target.data[i][j] % M
            # Solve a2 e^2 + a1 e + a0 - y ≡ 0 mod M
            A = a2 % M
            B = a1 % M
            C = (a0 - y) % M
            # Solve modulo prime powers
            rp = i + 1
            rq = j + 1
            Mp = p**rp
            Mq = q**rq
            roots_p = solve_quadratic_prime_power(A % Mp, B % Mp, C % Mp, p, rp)
            roots_q = solve_quadratic_prime_power(A % Mq, B % Mq, C % Mq, q, rq)
            for xp in roots_p:
                for xq in roots_q:
                    try:
                        xM, modM = crt_pair(xp, Mp, xq, Mq)
                    except Exception:
                        continue
                    if best_x is None:
                        best_x, best_m = xM, modM
                    else:
                        try:
                            best_x, best_m = crt_pair(best_x, best_m, xM, modM)
                        except Exception:
                            pass
    if best_x is None:
        return 0, 1
    return best_x, best_m


def attempt_decrypt(secret: int, ciphertext_hex: str):
    key = hashlib.sha256(hex(secret).encode()).digest()[:16]
    cipher = AES.new(key, AES.MODE_ECB)
    ct = bytes.fromhex(ciphertext_hex.strip())
    pt = cipher.decrypt(ct)
    try:
        return unpad(pt, 16).decode(errors="replace")
    except Exception:
        return pt.decode(errors="replace")


def main():
    if len(sys.argv) < 4:
        print("Usage: python solver_ring.py <g_file> <gexp_file> <cipher_hex>")
        print(
            "Place the exact printed matrices for g and g**secret into files, and supply ciphertext hex."
        )
        return
    with open(sys.argv[1], "r") as f:
        g_text = f.read()
    with open(sys.argv[2], "r") as f:
        gexp_text = f.read()
    cipher_hex = sys.argv[3]
    g = parse_matrix(g_text)
    gexp = parse_matrix(gexp_text)
    p, q = infer_p_q_from_mats(g, gexp)
    print(f"Inferred p bits: {p.bit_length()}, q bits: {q.bit_length()}")
    print("p =", p)
    print("q =", q)
    try:
        e_p2, e_q2, e_mod = recover_secret(p, q, g, gexp)
        print(f"e mod p^2 = {e_p2}")
        print(f"e mod q^2 = {e_q2}")
        print(f"CRT(e) mod p^2 q^2 = {e_mod}")
    except Exception as ex:
        print("Partial recovery failed:", ex)
        e_mod = 0
    # Note: Full e is needed for AES key; e_mod is insufficient. We still try.
    # First: partial via p-adic/q-adic logs on diagonal
    try:
        e_p2, e_q2, e_mod = recover_secret(p, q, g, gexp)
        print(f"e mod p^2 = {e_p2}")
        print(f"e mod q^2 = {e_q2}")
        print(f"CRT(e) mod p^2 q^2 = {e_mod}")
    except Exception as ex:
        print("Partial recovery (p/q-adic) failed:", ex)
        e_mod = 0
    # Second: attempt full recovery via linear lifting on off-diagonals
    e_lin, m_lin = full_recover_secret(p, q, g, gexp)
    print(f"Linear lifting: e ≡ {e_lin} (mod {m_lin})")
    # Combine residues if possible
    e_try = e_mod
    try:
        if m_lin and m_lin > 1:
            e_try, mod_try = crt_pair(e_mod, (p**2) * (q**2), e_lin, m_lin)
        else:
            mod_try = (p**2) * (q**2)
    except Exception:
        # fall back to strongest single residue
        if m_lin > (p**2) * (q**2):
            e_try = e_lin
            mod_try = m_lin
        else:
            e_try = e_mod
            mod_try = (p**2) * (q**2)
    # Third: attempt quadratic lifting for stronger modulus
    e_quad, m_quad = quadratic_lift_recover(p, q, g, gexp)
    print(f"Quadratic lifting: e ≡ {e_quad} (mod {m_quad})")
    try:
        if m_quad and m_quad > 1:
            e_try, mod_try = crt_pair(e_try, mod_try, e_quad, m_quad)
    except Exception:
        pass
    flag_guess = attempt_decrypt(e_try, cipher_hex)
    print("Decrypted guess:", flag_guess)


if __name__ == "__main__":
    main()
