#!/usr/bin/env python3
"""
Utility helpers for the SAYAKA_STREAM challenge.

Current features:
1. Recover the 3D plane noise from the published ciphertext stream.
2. Produce the de-noised keystream bits that come directly from the
   Sayaka generator (after the internal warm-up and the 1024-bit block
   that feeds the noise RNG).

The resulting binary blobs are saved under ``derived/`` so that they can
be re-used when experimenting with MT19937 state recovery or any other
attack strategy.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent
OUTPUT_TXT = ROOT / "output.txt"
DERIVED_DIR = ROOT / "derived"

N = 42
TOTAL_BITS = N ** 3


def idx(x: int, y: int, z: int) -> int:
    """Map (x, y, z) coordinates to a bit index (little endian)."""
    return x + y * N + z * N * N


def load_stream() -> Tuple[List[int], bytes]:
    """Load the published noisy keystream and the AES ciphertext."""
    stream_hex, cipher_hex = OUTPUT_TXT.read_text().strip().splitlines()
    stream_int = int(stream_hex, 16)
    bits = [(stream_int >> i) & 1 for i in range(TOTAL_BITS)]
    return bits, bytes.fromhex(cipher_hex)


def recover_plane_bits(bits: List[int]) -> Tuple[List[int], List[int], List[int]]:
    """
    Recover the three axis-aligned plane masks.

    For each axis we compare every slice with the reference slice that
    uses coordinate 0 on that axis. Because the underlying Sayaka stream
    is almost always 1, the majority vote gives the true plane bit with
    overwhelming confidence.
    """

    def reshape(data: List[int]) -> List[List[List[int]]]:
        return [
            [[data[idx(x, y, z)] for z in range(N)] for y in range(N)]
            for x in range(N)
        ]

    # D approximates the plane bits with ≈9% noise (flipped bits).
    D = [1 ^ b for b in bits]
    darr = reshape(D)

    planes_x = [0] * N
    planes_y = [0] * N
    planes_z = [0] * N

    def vote(delta: List[int]) -> int:
        score = sum(1 if bit else -1 for bit in delta)
        return 1 if score > 0 else 0

    # X planes (compare vs x = 0 reference slice).
    base_x = darr[0]
    for x in range(1, N):
        delta = [
            darr[x][y][z] ^ base_x[y][z] for y in range(N) for z in range(N)
        ]
        planes_x[x] = vote(delta)

    # Y planes (compare vs y = 0).
    for y in range(1, N):
        delta = [
            darr[x][y][z] ^ darr[x][0][z] for x in range(N) for z in range(N)
        ]
        planes_y[y] = vote(delta)

    # Z planes (compare vs z = 0).
    for z in range(1, N):
        delta = [
            darr[x][y][z] ^ darr[x][y][0] for x in range(N) for y in range(N)
        ]
        planes_z[z] = vote(delta)

    return planes_x, planes_y, planes_z


def materialize_noise(ax: List[int], ay: List[int], az: List[int]) -> List[int]:
    """Expand plane bits into the full 3D noise array."""
    noise = [0] * TOTAL_BITS
    for x in range(N):
        for y in range(N):
            base = ax[x] ^ ay[y]
            for z in range(N):
                noise[idx(x, y, z)] = base ^ az[z]
    return noise


def bits_to_bytes(bits: List[int], msb_first: bool = False) -> bytes:
    """Pack bits into bytes (padding the last byte with zeros if needed)."""
    if not msb_first:
        iterable = bits
    else:
        iterable = bits[::-1]
    out = bytearray()
    for i in range(0, len(iterable), 8):
        chunk = iterable[i : i + 8]
        value = 0
        for bit in chunk:
            value = (value << 1) | bit
        if len(chunk) < 8:
            value <<= 8 - len(chunk)
        out.append(value)
    return bytes(out)


def main() -> None:
    DERIVED_DIR.mkdir(exist_ok=True)
    noisy_bits, ciphertext = load_stream()
    ax, ay, az = recover_plane_bits(noisy_bits)
    noise_bits = materialize_noise(ax, ay, az)
    clean_bits = [b ^ n for b, n in zip(noisy_bits, noise_bits)]

    # Persist everything for later experiments.
    (DERIVED_DIR / "planes_x.bin").write_bytes(bytes(ax))
    (DERIVED_DIR / "planes_y.bin").write_bytes(bytes(ay))
    (DERIVED_DIR / "planes_z.bin").write_bytes(bytes(az))
    (DERIVED_DIR / "noise_bits.bin").write_bytes(bits_to_bytes(noise_bits))
    (DERIVED_DIR / "clean_bits_lsb.bin").write_bytes(bits_to_bytes(clean_bits))
    (DERIVED_DIR / "clean_bits_msb.bin").write_bytes(bits_to_bytes(clean_bits, msb_first=True))
    (DERIVED_DIR / "cipher.bin").write_bytes(ciphertext)

    print("Artifacts saved in", DERIVED_DIR)


if __name__ == "__main__":
    main()
