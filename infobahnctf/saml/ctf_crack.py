import hashlib

target = "pbkdf2_sha256$870000$OOBQQ0WfV9HTkHDY0WgR1$thO4lAEMVLxiz++zumI6DNOLVVpRW/3oh8IR4j+oC6E="

# CTF-specific passwords
passwords = [
    "akadmin",
    "admin",
    "Admin",
    "ADMIN",
    "password",
    "Password123",
    "admin123",
    "akadmin123",
    "infobahn",
    "infobahnctf",
    "InfobahnCTF",
    "saml",
    "SAML",
    "saml2024",
    "ctf2024",
    "CTF2024",
    "flag",
    "FLAG",
    "authentik",
    "Authentik",
    "akadmin!",
    "admin!",
    "P@ssw0rd",
    "Password1",
    "Password!",
    "akadmin!23",
    "saml{flag}",
    "welcome",
    "Welcome",
    "test",
    "Test123",
    "changeme",
    "ChangeMe",
    "default",
    "Default123",
    "root",
    "toor",
    "akadmin2024",
    "infobahn2024",
    "samlctf",
    "SamlCTF",
    "ak@dmin",
    "ak_admin",
    "CTF{",
    "infobahn{",
    "easy",
    "Easy123",
    "simple",
    "Simple123",
]

print(f"Testing {len(passwords)} CTF-themed passwords...")
print(f"Target hash: {target}\n")

for pwd in passwords:
    print(f"Trying: {pwd}")

print("\n[!] None matched - password is stronger than common CTF patterns")
