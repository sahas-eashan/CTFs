# Kyoko_Ring challenge solver

This folder contains a solver for the 3×3 mixed-(p,q)-adic ring challenge in `2nd one/challenge (4).py`.

What the challenge prints when run (on the organizer's side):
- line 1: the base element `g` (a 3×3 matrix of integers)
- line 2: `g**secret` (same format)
- line 3: AES-ECB ciphertext hex, using key = SHA-256(hex(secret))[:16]

The solver reconstructs the secret exponent `secret` modulo large powers of `p` and `q` using (p- and q-)adic logarithms and off-diagonal linear relations, and combines them with CRT. If needed, it attempts additional quadratic lifting.

## How to use

1) Capture the three outputs from running the challenge (exactly as printed) into a file, e.g. `out.txt`.
2) Copy the first line (matrix) into `g.txt` and the second line into `gexp.txt`. Copy the third line (hex) for the command below.
3) Run the solver:

```powershell
python .\solver_ring.py .\g.txt .\gexp.txt <ciphertext_hex>
```

It will print:
- inferred primes p and q (100-bit primes),
- residues of `secret` modulo p^2, q^2 and their CRT,
- any further residues found via linear/quadratic lifting,
- and a decrypted guess (if the recovered modulus uniquely determines the key).

If the recovered modulus is large enough to determine `secret` uniquely (≥ 2^580), the plaintext will be the flag and start with `infobahn{`.

If not, send me the `g`, `g**secret`, and ciphertext hex from the actual instance; I’ll plug them in and finish the recovery.

## Notes

- The default local run uses `FLAG=infobahn{fake_flag}`; solving your own local run will recover this placeholder flag, not the organizer’s real flag.
- The `solver_ring.py` does not require `p` and `q` inputs; it infers them from the matrix structure.
- Internally, it raises diagonals into principal-unit subgroups with `(p-1)` and `(q-1)` and applies a truncated p-adic log expansion to extract `secret mod p^2, q^2`, and uses linear (and optionally quadratic) fits on off-diagonals to increase the known modulus.
