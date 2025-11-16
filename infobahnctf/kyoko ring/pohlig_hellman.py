#!/usr/bin/env python3
import ast
from Crypto.Cipher import AES
from hashlib import sha256

print("[*] Computing n mod q using manual Pohlig-Hellman")

# Read data
with open(
    r"c:\Users\Cyborg\Documents\GitHub\CTFs\infobahnctf\kyoko ring\output (1).txt", "r"
) as f:
    lines = f.read().strip().splitlines()

g = ast.literal_eval(lines[0])
h = ast.literal_eval(lines[1])
cipher_hex = lines[2]

p = 1072623818971185563588378265409
q = 877884221210583981824110979993
n_mod_p = 208817068825597166772797503287

mod_q_g = [[x % q for x in row] for row in g]
mod_q_h = [[x % q for x in row] for row in h]

a = mod_q_g[0][0]
A = mod_q_h[0][0]

print(f"[+] a = {a}")
print(f"[+] A = {A}")
print(f"[+] Need to solve a^n ≡ A (mod q)")
print()

# q-1 = 2^3 * 19 * 5775554086911736722527045921
# Let's denote the large prime as P
P = 5775554086911736722527045921

print(f"[*] q-1 = 2^3 * 19 * {P}")
print(f"[*] Large prime P has {P.bit_length()} bits")
print()

# Step 1: n mod 8 (small, easy brute force)
print("[*] Computing n mod 8...")
g8 = pow(a, (q - 1) // 8, q)
h8 = pow(A, (q - 1) // 8, q)
n_mod_8 = None
for i in range(8):
    if pow(g8, i, q) == h8:
        n_mod_8 = i
        print(f"[+] n ≡ {i} (mod 8)")
        break

# Step 2: n mod 19 (small, easy brute force)
print("[*] Computing n mod 19...")
g19 = pow(a, (q - 1) // 19, q)
h19 = pow(A, (q - 1) // 19, q)
n_mod_19 = None
for i in range(19):
    if pow(g19, i, q) == h19:
        n_mod_19 = i
        print(f"[+] n ≡ {i} (mod 19)")
        break

# Step 3: n mod P (large prime - this is the hard part)
print(f"\n[*] Computing n mod {P} using baby-step giant-step...")
print(f"[!] This is a ~{P.bit_length()}-bit discrete log - will be VERY slow!")
print(f"[!] Estimated time: could take hours/days without optimization")
print()

# Baby-step giant-step parameters
import math

m = int(math.sqrt(P)) + 1  # ~2^32 steps
print(f"[*] Using m = {m} (needs ~{m.bit_length()} bits of memory)")
print(f"[*] This would require storing ~{m * 8 / (1024**3):.2f} GB of data")
print()

# This is impractical. Let me check if there's a shortcut...
# Maybe the secret is actually constrained differently?

print("[!] Full Pohlig-Hellman is impractical for this size")
print("[*] Trying alternative approach: checking if secret is small...")
print()

# What if the challenge author made the secret smaller than 580 bits?
# Or what if there's additional structure we can exploit?

# Let's try CRT with just the small factors
from sympy.ntheory.modular import crt

if n_mod_8 is not None and n_mod_19 is not None:
    n_small, mod_small = crt([8, 19], [n_mod_8, n_mod_19])
    print(f"[+] Using small factors: n ≡ {n_small} (mod {mod_small})")

    # Combined with n mod p
    n_combined, mod_combined = crt([p, mod_small], [n_mod_p, n_small])
    print(f"[+] Combined: n ≡ {n_combined} (mod {mod_combined})")
    print(f"[+] This gives ~{mod_combined.bit_length()} bits of the secret")
    print()

    # The secret was getrandbits(580), so up to 2^580
    # With ~107 bits known, we'd need to search 2^473 space - still impractical

    print(
        "[*] Searching small multiples (this likely won't work for 580-bit secret)..."
    )
    for k in range(1000):
        candidate = n_combined + k * mod_combined

        key = sha256(hex(candidate).encode()).digest()[:16]
        cipher = AES.new(key, AES.MODE_ECB)
        ciphertext = bytes.fromhex(cipher_hex)

        try:
            plaintext = cipher.decrypt(ciphertext)
            if b"infobahn{" in plaintext:
                print(f"\n{'='*60}")
                print(f"[+++] FLAG FOUND!")
                print(f"[+++] Secret = {candidate} ({candidate.bit_length()} bits)")
                print(f"[+++] Flag: {plaintext.decode('utf-8', errors='ignore')}")
                print(f"{'='*60}")
                exit(0)
        except:
            pass

print("\n[!] Simple search failed")
print("[*] This challenge likely requires:")
print("    1. Optimized baby-step giant-step for the large prime factor")
print("    2. Distributed computing / significant compute resources")
print("    3. Or there's additional structure/weakness we haven't found")
