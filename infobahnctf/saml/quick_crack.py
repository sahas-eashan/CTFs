import hashlib
import base64

stored_hash = "pbkdf2_sha256$870000$OOBQQ0WfV9HTkHDY0WgR1$thO4lAEMVLxiz++zumI6DNOLVVpRW/3oh8IR4j+oC6E="
algorithm, iterations, salt, hash_b64 = stored_hash.split("$")
iterations = int(iterations)
salt_bytes = salt.encode("utf-8")
expected_hash = base64.b64decode(hash_b64)

# Try very simple passwords
simple_passwords = [
    "",
    "a",
    "1",
    "0",
    "x",
    "admin1",
    "!",
    "akadmin1",
    "Akadmin1",
    "aaa",
    "111",
    "password1",
    "Admin1",
]

print("Testing very simple passwords...")
for pwd in simple_passwords:
    pwd_bytes = pwd.encode("utf-8")
    computed_hash = hashlib.pbkdf2_hmac("sha256", pwd_bytes, salt_bytes, iterations)
    if computed_hash == expected_hash:
        print(f"\n[+] PASSWORD FOUND: '{pwd}'\n")
        exit(0)
    print(f"Tried: '{pwd}'")

print("\n[-] None found")
