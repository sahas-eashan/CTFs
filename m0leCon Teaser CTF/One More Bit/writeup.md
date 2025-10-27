# One More Bit – Approximate FHE exploitation writeup

The service exposes an IND-CPA-D game built on CKKS. We get one encryption of either `m0` or `m1` and can run homomorphic circuits plus a restricted bit-decryption oracle: it returns a bit of the decrypted ciphertext if the same bit matches for both cleartexts; otherwise, we get a denial.

CKKS operates on approximate arithmetic, so decrypting the chosen ciphertext leaks small noise. When we encrypt pairs differing only slightly (e.g., `0.0` vs `1.0`), the least-significant bits of the fixed-point representation are equal, so the oracle answers. But the encrypted value drifts depending on whether `m0` or `m1` was chosen—noise accumulates differently. Sampling several low-order bits reveals a strong bias: the sum of observed ones is small when the challenger picked `m0`, large for `m1`.

Exploit steps per round:
- Send `{"command": "encrypt", "m0": 0.0, "m1": 1.0}` and note the returned `state_index`.
- Query `decrypt` on indices `0–23` for that ciphertext. All succeed because those bits match in both plaintexts. Collect the bits.
- If the sum of the 24 bits exceeds a threshold (≈6 in testing), guess `1`; otherwise guess `0`.

Repeating for 100 rounds wins the game, after which the server prints the flag.
