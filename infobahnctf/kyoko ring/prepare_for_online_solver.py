#!/usr/bin/env python3
"""
Generate discrete log problem parameters for online solvers
"""

import ast

print("=" * 70)
print("DISCRETE LOG PROBLEM FOR ONLINE SOLVERS")
print("=" * 70)

# Read data
with open(
    r"c:\Users\Cyborg\Documents\GitHub\CTFs\infobahnctf\kyoko ring\output (1).txt", "r"
) as f:
    lines = f.read().strip().splitlines()

g = ast.literal_eval(lines[0])
h = ast.literal_eval(lines[1])

p = 1072623818971185563588378265409
q = 877884221210583981824110979993

mod_q_g = [[x % q for x in row] for row in g]
mod_q_h = [[x % q for x in row] for row in h]

a = mod_q_g[0][0]
A = mod_q_h[0][0]

print("\nPROBLEM: Find n such that a^n ≡ A (mod q)")
print()
print(f"Base (a):     {a}")
print(f"Result (A):   {A}")
print(f"Modulus (q):  {q}")
print()
print("Factorization of q-1:")
print("  q-1 = 2^3 × 19 × 5775554086911736722527045921")
print()

# For Pohlig-Hellman, we need to solve in the large prime subgroup
P = 5775554086911736722527045921
print(f"HARD PART: Discrete log modulo large prime P = {P}")
print(f"  (This is a ~{P.bit_length()}-bit discrete log)")
print()

# Compute the generator and target in the subgroup of order P
g_P = pow(a, (q - 1) // P, q)
h_P = pow(A, (q - 1) // P, q)

print("Subgroup discrete log problem:")
print(f"  Find x such that g_P^x ≡ h_P (mod q)")
print(f"  where x is in range [0, {P-1}]")
print()
print(f"  g_P = {g_P}")
print(f"  h_P = {h_P}")
print(f"  q   = {q}")
print(f"  Order = {P}")
print()

print("=" * 70)
print("ONLINE TOOLS TO TRY:")
print("=" * 70)
print()
print("1. SageMath (https://sagecell.sagemath.org/)")
print("   Code:")
print("   ```")
print(f"   q = {q}")
print(f"   g = Mod({g_P}, q)")
print(f"   h = Mod({h_P}, q)")
print(f"   x = discrete_log(h, g)")
print("   print(x)")
print("   ```")
print()

print("2. Alpertron Discrete Log Calculator")
print("   (https://www.alpertron.com.ar/DILOG.HTM)")
print(f"   Base: {g_P}")
print(f"   Power: {h_P}")
print(f"   Modulus: {q}")
print()

print("3. PARI/GP")
print("   ```")
print(f"   q = {q}")
print(f"   g = Mod({g_P}, q)")
print(f"   h = Mod({h_P}, q)")
print("   x = znlog(h, g)")
print("   print(x)")
print("   ```")
print()

print("=" * 70)
print("AFTER GETTING x FROM ONLINE SOLVER:")
print("=" * 70)
print()
print("Run this to get the full secret and decrypt:")
print()
print("```python")
print("from sympy.ntheory.modular import crt")
print("from Crypto.Cipher import AES")
print("from hashlib import sha256")
print()
print(f"p = {p}")
print(f"q = {q}")
print(f"n_mod_p = {mod_q_g[0][0] if False else 208817068825597166772797503287}")
print("n_mod_8 = 0")
print("n_mod_19 = 5")
print(f"P = {P}")
print("n_mod_P = x  # <-- PUT THE RESULT FROM ONLINE SOLVER HERE")
print()
print("# Combine using CRT")
print("n_mod_152 = crt([8, 19], [0, 5])[0]  # = 24")
print("n_mod_q, _ = crt([152, P], [24, n_mod_P])")
print("secret, _ = crt([p, q], [n_mod_p, n_mod_q])")
print()
print("# Decrypt")
print(
    "cipher_hex = 'd372d0eb56a5c0c8e58022dd6786a069d9bad720b02139bb70283fa214ebce97d80f5c17ccb1af3eb20429a98a1ad13e07e3368a5444c5fac2846faf75a35000'"
)
print("key = sha256(hex(secret).encode()).digest()[:16]")
print("cipher = AES.new(key, AES.MODE_ECB)")
print("plaintext = cipher.decrypt(bytes.fromhex(cipher_hex))")
print("print(plaintext)")
print("```")
print()

print("=" * 70)
print("SAVE THIS TO A FILE FOR REFERENCE:")
print("=" * 70)

# Save to file
with open(
    r"c:\Users\Cyborg\Documents\GitHub\CTFs\infobahnctf\kyoko ring\dlog_problem.txt",
    "w",
    encoding="utf-8",
) as f:
    f.write(f"DISCRETE LOG PROBLEM\n")
    f.write(f"====================\n\n")
    f.write(f"Find x such that g^x = h (mod q)\n\n")
    f.write(f"g = {g_P}\n")
    f.write(f"h = {h_P}\n")
    f.write(f"q = {q}\n")
    f.write(f"order = {P}\n\n")
    f.write(f"SageMath code:\n")
    f.write(f"q = {q}\n")
    f.write(f"g = Mod({g_P}, q)\n")
    f.write(f"h = Mod({h_P}, q)\n")
    f.write(f"x = discrete_log(h, g)\n")
    f.write(f"print(x)\n")

print(f"\n[+] Problem parameters saved to dlog_problem.txt")
