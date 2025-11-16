#!/usr/bin/env python3
import ast
from Crypto.Cipher import AES
from hashlib import sha256
from sympy.ntheory.modular import crt
from sympy import discrete_log, factorint

print("[*] Kyoko Ring Challenge - Final Solver")
print()

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

# Part 1: n mod p (already computed)
n_mod_p = 208817068825597166772797503287
print(f"\n[+] n ≡ {n_mod_p} (mod p)")

# Part 2: n mod q using discrete log
print(f"\n[*] Computing n mod q using discrete logarithm...")
mod_q_g = [[x % q for x in row] for row in g]
mod_q_h = [[x % q for x in row] for row in h]

a = mod_q_g[0][0]
A = mod_q_h[0][0]

print(f"[*] Need to solve: {a}^n ≡ {A} (mod {q})")
print(f"[*] Factorization of q-1: {factorint(q-1)}")
print(f"[*] This will use Pohlig-Hellman algorithm...")

try:
    n_mod_q = discrete_log(q, A, a)
    print(f"[+] n ≡ {n_mod_q} (mod ord(a) | (q-1))")
except Exception as e:
    print(f"[-] Discrete log failed: {e}")
    print(f"[*] Trying alternative: using order computation...")
    # The order divides q-1
    phi = q - 1
    factors = factorint(phi)
    order_a = phi
    for prime, exp in factors.items():
        for _ in range(exp):
            if pow(a, order_a // prime, q) == 1:
                order_a //= prime
            else:
                break
    print(f"[*] Order of a: {order_a}")
    n_mod_q = discrete_log(q, A, a, order_a)
    print(f"[+] n ≡ {n_mod_q} (mod {order_a})")

# Part 3: Chinese Remainder Theorem
print(f"\n[*] Applying Chinese Remainder Theorem...")
secret, modulus = crt([p, q], [n_mod_p, n_mod_q])
print(f"[+] Secret n ≡ {secret} (mod {modulus})")
print(f"[+] Secret bit length: {secret.bit_length()} bits")

# Part 4: Decrypt the flag
print(f"\n[*] Decrypting the flag...")
key = sha256(hex(secret).encode()).digest()[:16]
cipher = AES.new(key, AES.MODE_ECB)
ciphertext = bytes.fromhex(cipher_hex)
plaintext = cipher.decrypt(ciphertext)

print(f"[+] Decrypted plaintext: {plaintext}")

if b"infobahn{" in plaintext:
    flag = plaintext.decode("utf-8", errors="ignore").strip()
    print(f"\n{'=' * 60}")
    print(f"[+] FLAG: {flag}")
    print(f"{'=' * 60}")
else:
    print(f"[-] Flag pattern not found, raw bytes: {plaintext.hex()}")
