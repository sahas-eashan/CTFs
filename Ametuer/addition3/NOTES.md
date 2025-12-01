# addition3 scratchpad

## Observations

- Plaintext template per query: `m = (flag << 512) + r + scramble (mod n)`.
- `flag << 512` is ~2^928; random mask `r` is <2^512.
- Modulus `n` is regenerated for every iteration via OpenSSL; public exponent hard-coded to `e = 3`.
- Returned ciphertext is `c = m^3 mod n` for a single randomly chosen message among 100k samples.
- Because `n` changes each query, cross-difference tricks from addition2 no longer apply.

## Exploration notes

- `n^(1/3)` is ~2^683, far below the base message size (~2^928). So naive cube-rooting never works without precise scrambling that cancels almost the entire flag contribution.
- Even completely canceling the high bits would require knowing `flag << 512` within roughly 683 bits. With only flag format knowledge, that's still too large to brute force.
- The equation `t^3 = c + k n` with `t = flag << 512 + r + scramble` might be exploitable: if we can identify the correct integer `k`, integer cube root yields the plaintext exactly, and `(t - scramble) >> 512` recovers the flag.
- Need a method to recover `k` without factoring `n`. Candidate approach: Coppersmith/LLL on `t^3 - c` with `t` constrained to share the same unknown but structured high bits across queries.

## Next steps

1. Build a local harness mirroring `chall.py` so we can iterate on attacks deterministically.
2. Model the Diophantine system `t^3 - c = k n` with `t = 2^512 * flag_value + r + scramble` and explore lattice-based recovery for small `r` and structured `flag_value`.
3. Once a viable recovery is demonstrated locally, wrap the attack in `solve_addition3.py` plus documentation and quick-run instructions.
