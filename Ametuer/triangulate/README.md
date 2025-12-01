# Triangulate Solver

This folder contains a standalone solver for the **amateursCTF 2024** challenge
`crypto/triangulate`.

## Approach

1. **Structure the leak.**  The challenge prints the states after the 1st, 3rd,
   6th, 10th, 15th, and 21st steps of an LCG with unknown parameters.  The step
   differences follow the triangular numbers (1, 2, 3, 4, 5, 6), so the usual
   consecutive-output tricks do not apply directly.
2. **Eliminate the increment.**  For any four consecutive leaked states we can
   combine the recurrences to obtain a polynomial `P_j(a)` that no longer
   depends on the increment `c`, only on the multiplier `a`.
3. **Recover the modulus.**  Every `P_j(a)` shares the same root `a` modulo the
   prime modulus `m`.  Therefore, the pairwise resultants of the polynomials are
   all multiples of `m`; taking the gcd of those resultants yields the prime
   modulus outright.
4. **Recover the multiplier and increment.**  Once `m` is known, factor any
   `P_j(a)` over GF(m) to obtain the linear factor `(a - A)` and read off the
   true multiplier.  A single leaked relation provides `c`, and the very first
   LCG step rewinds directly to the original seed (the flag).

## Usage

```
pip install -r requirements.txt
python solver.py            # uses the bundled six outputs
python solver.py -i dump.txt  # optional custom leak
```

The script prints `m`, `a`, `c`, and the recovered flag
`amateursCTF{w0w_such_cr3ativ3_lcG_ch4ll3ngE}`.

## Mini Writeup

1. Extract the six published states `S_{T_n}` where `T_n ∈ {1,3,6,10,15,21}`.
2. For each consecutive quadruple, derive `P_j(a)` that holds whenever the
   relation comes from a single LCG modulo `m`.  These are degree-4/5/6
   polynomials with integer coefficients.
3. Compute pairwise resultants of the `P_j(a)` polynomials and take their gcd;
   the only common factor is the prime modulus `m`.
4. Reduce any `P_j(a)` modulo `m` and factor it over GF(m); the linear factor
   yields the true multiplier `a`.
5. Solve for the increment `c` using one triangular-step relation, then invert
   the very first LCG step to recover the original seed/flag.
6. Convert the flag integer back to ASCII to reveal
   `amateursCTF{w0w_such_cr3ativ3_lcG_ch4ll3ngE}`.
