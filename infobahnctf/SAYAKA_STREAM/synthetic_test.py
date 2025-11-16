import random
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent))
from solve import (
    TOTAL_BITS,
    WARMUP_CALLS,
    recover_state,
    coords_for_prefix,
    START_INDEX,
    OBS_BITS,
)


def sayaka_bit(rng):
    x = rng.getrandbits(5)
    a, b, c, d, e = [(x >> i) & 1 for i in range(5)]
    return int((a or not b or c == d or d != e) and (not a or b or c or d or not e))


def generate_instance():
    n = 42
    secret = random.getrandbits(19936)
    rng = random.Random(secret)
    for _ in range(WARMUP_CALLS):
        rng.getrandbits(5)
    state_after = rng.getstate()

    bits = [sayaka_bit(rng) for _ in range(TOTAL_BITS)]
    stream_int = 0
    for b in bits:
        stream_int = (stream_int << 1) | b

    # deterministic noise using same routine as challenge
    noise_seed = 0  # irrelevant for this synthetic check; keep zero mask
    noise = 0
    output_int = stream_int ^ noise

    bits_lsb = [(output_int >> i) & 1 for i in range(TOTAL_BITS)]
    bits_msb = list(reversed(bits_lsb))
    return secret, state_after, bits_msb


def main():
    secret, actual_state, bits = generate_instance()
    obs = bits[:OBS_BITS]
    coords = coords_for_prefix(len(obs))
    recovered_state, _, _, _ = recover_state(obs, coords)
    ok = list(actual_state[1][:-1]) == recovered_state and actual_state[1][-1] == (
        START_INDEX % TOTAL_BITS
    )
    print("state matches?", ok)


if __name__ == "__main__":
    main()
