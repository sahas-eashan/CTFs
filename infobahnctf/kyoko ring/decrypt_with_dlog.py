#!/usr/bin/env python3
"""
Final decryption script - USE AFTER GETTING x FROM SAGEMATH
"""

from sympy.ntheory.modular import crt
from Crypto.Cipher import AES
from hashlib import sha256

print("=" * 70)
print("FINAL DECRYPTION SCRIPT")
print("=" * 70)
print()

# Known values
p = 1072623818971185563588378265409
q = 877884221210583981824110979993
n_mod_p = 208817068825597166772797503287
n_mod_8 = 0
n_mod_19 = 5
P = 5775554086911736722527045921

print("Enter the discrete log result from SageMath:")
print("(The value of x where g^x = h mod q)")
n_mod_P_input = input("x = ").strip()

try:
    n_mod_P = int(n_mod_P_input)
except:
    print("Invalid input! Must be an integer.")
    exit(1)

print()
print(f"[+] Using n_mod_P = {n_mod_P}")
print()

# Step 1: Combine small factors
print("[*] Step 1: Combining small factors (8 and 19)...")
n_mod_152, mod_152 = crt([8, 19], [n_mod_8, n_mod_19])
print(f"    n ≡ {n_mod_152} (mod {mod_152})")

# Step 2: Combine with large prime
print("[*] Step 2: Combining with large prime subgroup...")
n_mod_q, mod_q_full = crt([mod_152, P], [n_mod_152, n_mod_P])
print(f"    n ≡ {n_mod_q} (mod q-1)")

# Step 3: Final CRT with p and q
print("[*] Step 3: Final CRT to get full secret...")
secret, modulus = crt([p, q], [n_mod_p, n_mod_q])
print(f"    Secret ≡ {secret} (mod {modulus})")
print(f"    Secret bit length: {secret.bit_length()} bits")
print()

# Step 4: Decrypt
print("[*] Step 4: Decrypting flag...")
cipher_hex = "d372d0eb56a5c0c8e58022dd6786a069d9bad720b02139bb70283fa214ebce97d80f5c17ccb1af3eb20429a98a1ad13e07e3368a5444c5fac2846faf75a35000"
key = sha256(hex(secret).encode()).digest()[:16]
cipher = AES.new(key, AES.MODE_ECB)
ciphertext = bytes.fromhex(cipher_hex)

try:
    plaintext = cipher.decrypt(ciphertext)
    print(f"[+] Decrypted bytes: {plaintext}")
    print()

    if b"infobahn{" in plaintext or b"CTF{" in plaintext:
        flag = plaintext.decode("utf-8", errors="ignore").strip()
        print("=" * 70)
        print("FLAG FOUND!")
        print("=" * 70)
        print(flag)
        print("=" * 70)
    else:
        print("[!] Decryption successful but flag pattern not found")
        print(f"[!] Raw hex: {plaintext.hex()}")
except Exception as e:
    print(f"[-] Decryption failed: {e}")
    print("[!] The discrete log value might be incorrect")
