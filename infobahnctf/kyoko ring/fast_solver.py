#!/usr/bin/env python3
import ast
from Crypto.Cipher import AES
from hashlib import sha256
from sympy.ntheory.modular import crt

print("[*] Kyoko Ring Challenge - Fast Solver")

# Read output
with open(
    r"c:\Users\Cyborg\Documents\GitHub\CTFs\infobahnctf\kyoko ring\output (1).txt", "r"
) as f:
    lines = f.read().strip().splitlines()

g = ast.literal_eval(lines[0])
h = ast.literal_eval(lines[1])
cipher_hex = lines[2]

# Recovered primes
p = 1072623818971185563588378265409
q = 877884221210583981824110979993

print(f"[+] p = {p} ({p.bit_length()} bits)")
print(f"[+] q = {q} ({q.bit_length()} bits)")

# n mod p (from unipotent matrix analysis)
n_mod_p = 208817068825597166772797503287
print(f"[+] n ≡ {n_mod_p} (mod p)")

# For n mod q, we use the sum formula instead of full discrete log
print(f"\n[*] Computing n mod q using algebraic structure...")
mod_q_g = [[x % q for x in row] for row in g]
mod_q_h = [[x % q for x in row] for row in h]

a = mod_q_g[0][0]  # = 631485148960453814978234000583
d = mod_q_g[1][1]  # = 595668279275061484652722023259
A = mod_q_h[0][0]  # = 851543954053199974308376397696
D = mod_q_h[1][1]  # = 739550752202716103916296732687

# We have: A = a^n, D = d^n (mod q)
# The sum S = (A - D) / (a - d) = sum_{i=0}^{n-1} a^(n-1-i) * d^i
# This equals (a^n - d^n) / (a - d)

# From our earlier analysis, we found S = 386716056001903326238792695372
# And we know this sum has a specific relationship with n

# Alternative: use the ratio r = a/d
# r^n = A/D (mod q)
# So we need discrete log base r

r = (a * pow(d, -1, q)) % q
R = (A * pow(D, -1, q)) % q

print(f"[*] Computing discrete log for ratio...")
print(f"[*] r = {r}")
print(f"[*] R = {R}")

# The order of r divides q-1 = 8 * 19 * 5775554086911736722527045921
# Let's check if r has order 19 (much smaller!)

print(f"[*] Checking order of r...")
for d in [2, 4, 8, 19, 38, 76, 152]:
    val = pow(r, (q - 1) // d, q)
    if val == 1:
        print(f"    r^((q-1)/{d}) = 1, so order divides (q-1)/{d}")

# r has order 19! So we can do discrete log in a group of order 19
print(f"\n[*] r has small order! Computing discrete log modulo order...")

# Since r^19 = 1, we solve r^n ≡ R (mod q) where n is taken mod 19
from sympy import discrete_log

order_r = 19
try:
    n_mod_19 = discrete_log(order_r, R % q, r)
    print(f"[+] n ≡ {n_mod_19} (mod 19)")
except:
    # Brute force for order 19
    print(f"[*] Brute forcing n mod 19...")
    for i in range(19):
        if pow(r, i, q) == R:
            n_mod_19 = i
            print(f"[+] n ≡ {n_mod_19} (mod 19)")
            break

# Now we have n mod p and n mod 19
# We can use CRT, but we need n mod (q-1) or at least a larger modulus
# Since the order of elements mod q divides q-1, we actually have n mod order

# Let's try: secret was 580 bits, so we need more info
# Let's compute n modulo larger factors of q-1

print(f"\n[*] Working with larger subgroups...")

# Check the element 'a' itself
# Order of a divides q-1 = 2^3 * 19 * 5775554086911736722527045921
# From earlier analysis: order of a is 109735527651322997728013872499

# Let's use a baby-step giant-step for small discrete logs
# Or we can use the structure more directly

# Since we have limited information, let's try a meet-in-the-middle approach
# The secret is ~580 bits, n mod p is known, n mod 19 is known

# CRT with p and 19:
from math import gcd as math_gcd

if math_gcd(p, 19) == 1:
    n_partial, mod_partial = crt([p, 19], [n_mod_p, n_mod_19])
    print(f"[+] n ≡ {n_partial} (mod {mod_partial})")
    print(f"[+] This gives ~{mod_partial.bit_length()} bits of information")

# Since secret is ~580 bits and we have ~100 bits from mod p,
# we still need to search ~480 bits worth
# BUT the secret was generated with getrandbits(580), not uniformly in range
# So let's try small multipliers

print(f"\n[*] Trying candidate secrets...")

max_tries = 100000
for k in range(max_tries):
    candidate = n_partial + k * mod_partial

    # Check if it matches our constraints
    if candidate % 19 != n_mod_19:
        continue
    if candidate % p != n_mod_p:
        continue

    # Try to decrypt
    key = sha256(hex(candidate).encode()).digest()[:16]
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = bytes.fromhex(cipher_hex)

    try:
        plaintext = cipher.decrypt(ciphertext)
        if (
            b"infobahn{" in plaintext
            or b"CTF{" in plaintext
            or b"flag" in plaintext.lower()
        ):
            print(f"\n{'='*60}")
            print(f"[+] FLAG FOUND!")
            print(f"[+] k = {k}")
            print(f"[+] Secret = {candidate}")
            print(f"[+] Secret bits = {candidate.bit_length()}")
            print(f"[+] Plaintext: {plaintext}")
            print(f"{'='*60}")
            exit(0)
    except:
        pass

    if k % 10000 == 0 and k > 0:
        print(f"    Tested {k} candidates, current bits: {candidate.bit_length()}")

    if candidate.bit_length() > 600:
        print(f"[!] Exceeded expected bit length")
        break

print(f"[-] Flag not found in {max_tries} attempts")
print(f"[*] May need more sophisticated discrete log or different approach")
