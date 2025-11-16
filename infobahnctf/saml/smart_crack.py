import hashlib
import base64

# Target hash from database
target = "pbkdf2_sha256$870000$OOBQQ0WfV9HTkHDY0WgR1$thO4lAEMVLxiz++zumI6DNOLVVpRW/3oh8IR4j+oC6E="

# Parse the hash
parts = target.split('$')
algorithm = parts[0]
iterations = int(parts[1])
salt = parts[2]
expected_hash = parts[3]

print(f"Algorithm: {algorithm}")
print(f"Iterations: {iterations}")
print(f"Salt: {salt}")
print(f"Expected hash: {expected_hash}")
print(f"\nCracking with smart wordlist...")
print("=" * 60)

# Read wordlist
with open('smart_wordlist.txt', 'r', encoding='utf-8') as f:
    passwords = [line.strip() for line in f if line.strip()]

tested = 0
for password in passwords:
    tested += 1
    # Django's PBKDF2 implementation
    hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), iterations)
    hash_b64 = base64.b64encode(hash_obj).decode('ascii').rstrip('=')
    
    if hash_b64 == expected_hash:
        print(f"\n[+] PASSWORD FOUND: {password}")
        print(f"[+] Tested {tested} passwords")
        exit(0)
    
    if tested % 10 == 0:
        print(f"Tested {tested}/{len(passwords)}: {password}")

print(f"\n[-] Password not found in wordlist ({tested} passwords tested)")
print("[!] Try a larger wordlist or more iterations")
