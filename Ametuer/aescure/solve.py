from Crypto.Cipher import AES
import itertools
import string

# The ciphertext given in the challenge
target_hex = "5aed095b21675ec4ceb770994289f72b"
target_ct = bytes.fromhex(target_hex)

# The plaintext used in the challenge
pt = b"\x00" * 16

# Known parts of the flag
prefix = "amateursCTF{"
suffix = "}"

# 16 bytes (AES-128) - 12 bytes (prefix) - 1 byte (suffix) = 3 bytes to guess
missing_length = 16 - len(prefix) - len(suffix)

print(f"[*] Brute forcing {missing_length} missing characters...")

# Create a character set (digits, letters, and common symbols)
charset = string.digits + string.ascii_letters + "_!@#$%^&*()-+"

found = False

for guess_tuple in itertools.product(charset, repeat=missing_length):
    guess = "".join(guess_tuple)
    candidate_key = prefix + guess + suffix

    # The key must be bytes
    key_bytes = candidate_key.encode()

    try:
        # Replicate the challenge encryption
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        encrypted = cipher.encrypt(pt)

        if encrypted == target_ct:
            print(f"\n[+] FLAG FOUND: {candidate_key}")
            found = True
            break
    except ValueError:
        # Ignores keys that don't meet length requirements if we messed up math
        continue

if not found:
    print("[-] Flag not found. Try expanding the charset (e.g. string.printable).")
