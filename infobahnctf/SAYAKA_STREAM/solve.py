#!/usr/bin/env python3
"""
Solver for the SAYAKA_STREAM challenge.

Pipeline:
1. Reconstruct the clean Sayaka keystream bits (noise-free) using the
   algebraic recovery from analyze.py.
2. Use a bit-vector SAT instance (z3) to recover the MT19937 state of the
   Python Random object at the moment the keystream begins (after the warm-up
   + 1024-bit noise seed extraction).
3. (Next steps: rewind the generator back to the seeding phase, invert
   init_by_array, recover the original 19936-bit seed, derive the AES key,
   and decrypt the flag.)
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

from z3 import (
    BitVec,
    BitVecVal,
    BoolVal,
    If,
    LShR,
    Or,
    SolverFor,
    And,
    sat,
)

from analyze import load_stream, recover_plane_bits, materialize_noise, TOTAL_BITS

# --- Constants ---------------------------------------------------------------

N = 42
STREAM_BITS = N**3  # 74088 bits

MT_N = 624
MT_M = 397
MATRIX_A = 0x9908B0DF
UPPER_MASK = 0x80000000
LOWER_MASK = 0x7FFFFFFF
UPPER_MASK_BV = BitVecVal(UPPER_MASK, 32)
LOWER_MASK_BV = BitVecVal(LOWER_MASK, 32)
MATRIX_A_BV = BitVecVal(MATRIX_A, 32)
ZERO32 = BitVecVal(0, 32)

WARMUP_CALLS = 10**5 + 1024  # generator bits consumed before returned stream
START_INDEX = WARMUP_CALLS % MT_N  # pointer position at first returned bit

OBS_BITS = 3500  # number of keystream bits fed to z3


ZERO_TOP_VALUES = [BitVecVal(v, 32) for v in (6, 17, 26)]


# --- Helpers ----------------------------------------------------------------

def reconstruct_clean_bits() -> Tuple[List[int], bytes]:
    noisy_bits, ciphertext = load_stream()
    ax, ay, az = recover_plane_bits(noisy_bits)
    noise_bits = materialize_noise(ax, ay, az)
    clean_bits_lsb = [b ^ n for b, n in zip(noisy_bits, noise_bits)]
    clean_bits = list(reversed(clean_bits_lsb))
    return clean_bits, ciphertext


def mt_temper(x: BitVec) -> BitVec:
    y = x
    y ^= LShR(y, 11)
    y ^= (y << 7) & BitVecVal(0x9D2C5680, 32)
    y ^= (y << 15) & BitVecVal(0xEFC60000, 32)
    y ^= LShR(y, 18)
    return y


def build_state_cycles(num_cycles: int, solver) -> List[List[BitVec]]:
    state_cycles = []
    for cyc in range(num_cycles):
        state_cycles.append([BitVec(f"s_{cyc}_{i}", 32) for i in range(MT_N)])
    solver.add(Or(*[state_cycles[0][i] != 0 for i in range(MT_N)]))
    for cyc in range(num_cycles - 1):
        curr = state_cycles[cyc]
        nxt = state_cycles[cyc + 1]
        for i in range(MT_N):
            y = (curr[i] & UPPER_MASK_BV) | (curr[(i + 1) % MT_N] & LOWER_MASK_BV)
            val = curr[(i + MT_M) % MT_N] ^ LShR(y, 1)
            val ^= If((y & BitVecVal(1, 32)) == BitVecVal(1, 32), MATRIX_A_BV, ZERO32)
            solver.add(nxt[i] == val)
    return state_cycles


def recover_state(observations: List[int]) -> List[int]:
    solver = SolverFor("QF_BV")
    total_needed = START_INDEX + len(observations)
    num_cycles = (total_needed + MT_N - 1) // MT_N
    state_cycles = build_state_cycles(num_cycles, solver)

    for pos, bit in enumerate(observations):
        absolute = START_INDEX + pos
        cyc = absolute // MT_N
        offset = absolute % MT_N
        tempered = mt_temper(state_cycles[cyc][offset])
        top5 = LShR(tempered, 27)
        if bit == 0:
            solver.add(Or(*[top5 == val for val in ZERO_TOP_VALUES]))
        else:
            solver.add(And(*[top5 != val for val in ZERO_TOP_VALUES]))

    status = solver.check()
    if status != sat:
        raise RuntimeError(f"z3 failed (status={status}, reason={solver.reason_unknown()})")
    model = solver.model()
    return [model.evaluate(state_cycles[0][i]).as_long() & 0xFFFFFFFF for i in range(MT_N)]


def main():
    clean_bits, ciphertext = reconstruct_clean_bits()
    observations = clean_bits[:OBS_BITS]
    state = recover_state(observations)
    print("Recovered MT state for start of stream.")
    print("First few words:", state[:5])
    print("Ciphertext len:", len(ciphertext))


if __name__ == "__main__":
    main()
