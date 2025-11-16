#!/usr/bin/env python3
import ast
from Crypto.Cipher import AES
from hashlib import sha256
from math import gcd
from functools import reduce

print("[*] Kyoko Ring Challenge Solver")
print("[*] Reading output file...")

with open(
    r"c:\Users\Cyborg\Documents\GitHub\CTFs\infobahnctf\kyoko ring\output (1).txt", "r"
) as f:
    lines = f.read().strip().splitlines()

g = ast.literal_eval(lines[0])
h = ast.literal_eval(lines[1])
ciphertext = bytes.fromhex(lines[2])

print("[+] Step 1: Recovering primes p and q from GCD analysis")
p_candidates = [g[1][0], g[2][0], g[2][1]]
q_candidates = [g[0][1], g[0][2], g[1][2]]

p = reduce(gcd, [abs(int(x)) for x in p_candidates])
q = reduce(gcd, [abs(int(x)) for x in q_candidates])

print(f"[+] p = {p}")
print(f"[+] q = {q}")
print(f"[+] p is {p.bit_length()} bits, q is {q.bit_length()} bits")

print("\n[+] Step 2: Extracting secret modulo p")
mod_p_g = [[x % p for x in row] for row in g]
mod_p_h = [[x % p for x in row] for row in h]

# Diagonal factorization: G = D * U
D = [mod_p_g[i][i] for i in range(3)]
invD = [pow(D[i], -1, p) for i in range(3)]
U = [[(invD[i] * mod_p_g[i][j]) % p for j in range(3)] for i in range(3)]

D_n = [mod_p_h[i][i] for i in range(3)]
invD_n = [pow(D_n[i], -1, p) for i in range(3)]
U_n = [[(invD_n[i] * mod_p_h[i][j]) % p for j in range(3)] for i in range(3)]

# For unipotent upper triangular: U^n[i][j] follows specific patterns
# U^n[0][1] = n * U[0][1]
# U^n[1][2] = n * U[1][2]
n_mod_p = (U_n[0][1] * pow(U[0][1], -1, p)) % p
print(f"[+] n ≡ {n_mod_p} (mod p)")

# Verify with another position
n_check = (U_n[1][2] * pow(U[1][2], -1, p)) % p
if n_check != n_mod_p:
    print(f"[!] Warning: inconsistent n mod p: {n_check} != {n_mod_p}")
    print(f"[!] This means the unipotent formula is more complex")

print("\n[+] Step 3: Using Chinese Remainder Theorem approach")
print(f"[*] Secret is approximately 580 bits")
print(f"[*] With n mod p known, searching for full secret...")

# The secret n = n_mod_p + k*p for some k
# Since secret is ~580 bits and p is ~100 bits, k is roughly 480 bits
# But we can try smaller values first

print("\n[+] Trying direct values and small multiples...")
test_count = 0
max_k = 1000000

for k in range(max_k):
    candidate = n_mod_p + k * p

    if k % 100000 == 0 and k > 0:
        print(
            f"[*] Tested {k} candidates, current bit length: {candidate.bit_length()}"
        )

    if candidate.bit_length() > 600:
        print(f"[!] Exceeded expected bit length at k={k}")
        break

    key = sha256(hex(candidate).encode()).digest()[:16]
    cipher = AES.new(key, AES.MODE_ECB)

    try:
        plaintext = cipher.decrypt(ciphertext)
        # Check for flag patterns
        if b"infobahn{" in plaintext or b"flag" in plaintext.lower():
            print(f"\n[+] *** FLAG FOUND! ***")
            print(f"[+] k = {k}")
            print(f"[+] Secret = {candidate}")
            print(f"[+] Secret bit length = {candidate.bit_length()}")
            print(f"[+] Flag: {plaintext.decode('utf-8', errors='backslashreplace')}")
            exit(0)
    except Exception:
        pass

    test_count += 1

print(f"\n[-] Flag not found after testing {test_count} candidates")
print(
    "[*] The secret might require a different approach (e.g., full discrete log modulo q)"
)
