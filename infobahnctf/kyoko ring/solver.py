import ast
from Crypto.Cipher import AES
from hashlib import sha256
from math import gcd
from functools import reduce

# Read output
with open(
    r"c:\Users\Cyborg\Documents\GitHub\CTFs\infobahnctf\kyoko ring\output (1).txt", "r"
) as f:
    lines = f.read().strip().splitlines()

g = ast.literal_eval(lines[0])
h = ast.literal_eval(lines[1])
ciphertext = bytes.fromhex(lines[2])

# Step 1: Extract primes p and q from GCD analysis
p_candidates = [g[1][0], g[2][0], g[2][1]]
q_candidates = [g[0][1], g[0][2], g[1][2]]

p = reduce(gcd, [abs(int(x)) for x in p_candidates])
q = reduce(gcd, [abs(int(x)) for x in q_candidates])

print(f"Recovered p: {p}")
print(f"Recovered q: {q}")

# Step 2: Work modulo p to extract the secret exponent
# Reduce matrices modulo p
mod_p_g = [[x % p for x in row] for row in g]
mod_p_h = [[x % p for x in row] for row in h]

# Extract diagonal elements
D = [mod_p_g[i][i] for i in range(3)]
invD = [pow(D[i], -1, p) for i in range(3)]

# Compute left-normalized unipotent matrix U = D^{-1} * G
U = [[(invD[i] * mod_p_g[i][j]) % p for j in range(3)] for i in range(3)]

# Compute U^n = D_n^{-1} * H
D_n = [mod_p_h[i][i] for i in range(3)]
invD_n = [pow(D_n[i], -1, p) for i in range(3)]
U_n = [[(invD_n[i] * mod_p_h[i][j]) % p for j in range(3)] for i in range(3)]

# For unipotent upper triangular matrices, U^n has simple structure
# U^n[0][1] = n * U[0][1] and U^n[1][2] = n * U[1][2]
u_01 = U[0][1]
u_12 = U[1][2]
un_01 = U_n[0][1]
un_12 = U_n[1][2]

# Extract n mod p
n_mod_p_1 = (un_01 * pow(u_01, -1, p)) % p
n_mod_p_2 = (un_12 * pow(u_12, -1, p)) % p

print(f"\nn mod p from U[0][1]: {n_mod_p_1}")
print(f"n mod p from U[1][2]: {n_mod_p_2}")

# Use the first one (they should be consistent mod p)
n_mod_p = n_mod_p_1

# Step 3: Work modulo q to extract n mod q
mod_q_g = [[x % q for x in row] for row in g]
mod_q_h = [[x % q for x in row] for row in h]

a = mod_q_g[0][0]
d = mod_q_g[1][1]
A = mod_q_h[0][0]
D = mod_q_h[1][1]

# For the diagonal structure modulo q:
# A = a^n, D = d^n
# (A - D) / (a - d) gives us a sum related to n
inv_diff = pow((a - d) % q, -1, q)
S = ((A - D) % q * inv_diff) % q

# Verify using off-diagonal
c1 = mod_q_g[1][0]
S_check = (mod_q_h[1][0] * pow(c1, -1, q)) % q
print(f"\nS from diagonal: {S}")
print(f"S from off-diagonal: {S_check}")

# Now we need to solve for n modulo q from the relationship
# This is more complex; let's use a discrete log approach
# Since we have constraints, we can use CRT after finding n mod q

# For now, let's try small values or use the structure
# Actually, let's reconstruct using CRT with what we have

# Step 4: Use Chinese Remainder Theorem
# We have n ≡ n_mod_p (mod p)
# We need n mod q as well

# Let's try a different approach: the secret is 580 bits
# Let's search for n using the constraint that it's ~580 bits
# and matches our modulo p constraint

print(f"\nSearching for secret (this may take a moment)...")

# The secret is getrandbits(580), so it's up to 2^580
# But we have n mod p, so we can search: n = n_mod_p + k*p for small k
# Given the secret is ~580 bits and p is ~100 bits, k is at most 2^480

# Let's verify our n_mod_p first by checking if g^n_mod_p matches h modulo small checks
# Actually, let's try to find n mod (p-1) or use the factorization approach

# Alternative: Since we found n mod p, let's try to verify with small multiples
test_secret = n_mod_p
print(f"\nTrying secret: {test_secret}")

# Test decryption
key = sha256(hex(test_secret).encode()).digest()[:16]
cipher = AES.new(key, AES.MODE_ECB)
try:
    plaintext = cipher.decrypt(ciphertext)
    print(f"Decrypted: {plaintext}")
    if b"infobahn{" in plaintext:
        print(f"\n*** FLAG FOUND: {plaintext.decode('utf-8', errors='ignore')} ***")
except Exception as e:
    print(f"Decryption failed: {e}")

# If that doesn't work, search for n = n_mod_p + k*p
print("\nSearching with CRT approach...")
for k in range(10000):
    candidate = n_mod_p + k * p
    if candidate.bit_length() > 600:
        break

    if k % 1000 == 0:
        print(f"Trying k={k}, candidate bit length: {candidate.bit_length()}")

    key = sha256(hex(candidate).encode()).digest()[:16]
    cipher = AES.new(key, AES.MODE_ECB)
    try:
        plaintext = cipher.decrypt(ciphertext)
        if b"infobahn{" in plaintext or b"CTF{" in plaintext or b"flag" in plaintext:
            print(f"\n*** FLAG FOUND with k={k} ***")
            print(f"Secret: {candidate}")
            print(f"Flag: {plaintext.decode('utf-8', errors='ignore')}")
            break
    except:
        pass
