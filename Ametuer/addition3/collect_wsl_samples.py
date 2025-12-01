#!/usr/bin/env python3
"""
Collect samples for lattice attack
Run in Windows Python, saves for WSL processing
"""

from pwn import remote
import time

HOST = "amt.rs"
PORT = 35077
SAMPLES = 10  # Collect multiple samples

samples = []

for i in range(SAMPLES):
    try:
        io = remote(HOST, PORT, level='error')

        # Get n, e
        line = io.recvline().decode()
        n_str, e_str = line.split("=")[1].strip()[1:-1].split(",")
        n = int(n_str.strip())
        e = int(e_str.strip())

        # Query with scramble = 0
        io.recvuntil(b"scramble the flag: ")
        io.sendline(b"0")
        io.recvuntil(b"scrambling...\n")
        c_line = io.recvline().decode()
        c = int(c_line.split("=")[1].strip())

        samples.append((n, e, c))
        io.close()

        print(f"Sample {i+1}/{SAMPLES} collected: n={n.bit_length()} bits")
        time.sleep(1)  # Be nice to the server

    except Exception as ex:
        print(f"Failed to collect sample {i+1}: {ex}")
        break

# Save in format for WSL
with open("wsl_samples.txt", "w") as f:
    for idx, (n, e, c) in enumerate(samples):
        f.write(f"# Sample {idx}\n")
        f.write(f"n_{idx} = {n}\n")
        f.write(f"e_{idx} = {e}\n")
        f.write(f"c_{idx} = {c}\n")
        f.write("\n")

print(f"\nSaved {len(samples)} samples to wsl_samples.txt")
print("Now run: wsl python3 lattice_attack.py")
