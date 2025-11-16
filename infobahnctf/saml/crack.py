import hashlib
import base64

target_hash = "pbkdf2_sha256$870000$OOBQQ0WfV9HTkHDY0WgR1$thO4lAEMVLxiz++zumI6DNOLVVpRW/3oh8IR4j+oC6E="

# Parse the hash
parts = target_hash.split("$")
algorithm = parts[0]
iterations = int(parts[1])
salt = parts[2]
expected_hash = parts[3]

print(f"[*] Algorithm: {algorithm}")
print(f"[*] Iterations: {iterations}")
print(f"[*] Salt: {salt}")
print(f"[*] Target hash: {expected_hash}\n")


def check_password(password):
    # PBKDF2-HMAC-SHA256
    dk = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), iterations
    )
    computed = base64.b64encode(dk).decode("ascii")
    return computed == expected_hash


# Read wordlist
with open("wordlist.txt", "r", encoding="utf-8") as f:
    passwords = [line.strip() for line in f if line.strip()]

print(f"[*] Testing {len(passwords)} passwords...")
print(f"[*] This will take a while with {iterations} iterations...\n")

for i, pwd in enumerate(passwords, 1):
    if i % 10 == 0:
        print(f"[*] Progress: {i}/{len(passwords)} - Testing: {pwd[:20]}...")

    if check_password(pwd):
        print(f"\n[+] PASSWORD FOUND: {pwd}")
        exit(0)

print("\n[-] Password not found in wordlist")
