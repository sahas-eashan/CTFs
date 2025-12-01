#!/usr/bin/env python3
"""
Collects (n, c) samples from the addition3 challenge for lattice/Coppersmith attack.
Run this script and save the output for use in SageMath/fpylll in WSL.
"""

from pwn import remote
import time

HOST = "amt.rs"
PORT = 33779
SAMPLES = 50  # Increase for more reliability
SCRAMBLE = 0

samples = []

for i in range(SAMPLES):
    io = remote(HOST, PORT)
    n_e_line = io.recvline().decode()
    n_str, e_str = n_e_line.split("=")[1].strip()[1:-1].split(",")
    n = int(n_str.strip())
    e = int(e_str.strip())
    io.recvuntil(b"scramble the flag: ")
    io.sendline(str(SCRAMBLE).encode())
    io.recvuntil(b"scrambling...\n")
    c_line = io.recvline().decode()
    c = int(c_line.split("=")[1].strip())
    samples.append((n, e, c))
    io.close()
    print(f"Sample {i+1}/{SAMPLES} collected.")
    time.sleep(0.2)  # Avoid hammering the server

with open("samples.txt", "w") as f:
    for n, e, c in samples:
        f.write(f"n = {n}\ne = {e}\nc = {c}\n\n")

print(
    f"\nSaved {SAMPLES} samples to samples.txt. Use this file in SageMath/fpylll for the lattice attack."
)
