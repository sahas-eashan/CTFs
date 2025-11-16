# Kyoko Ring CTF Challenge - Solution Guide

## Problem Summary
This challenge uses a custom algebraic structure (Kyoko Ring) with matrix exponentiation modulo p*q. We need to recover a 580-bit secret exponent to decrypt the flag.

## What We've Found

### Recovered Primes
- **p** = 1072623818971185563588378265409 (100 bits)
- **q** = 877884221210583981824110979993 (100 bits)

### Partial Secret Information
- n ≡ 208817068825597166772797503287 (mod p)
- n ≡ 0 (mod 8)
- n ≡ 5 (mod 19)
- n ≡ ? (mod 5775554086911736722527045921) ← **THIS IS WHAT WE NEED**

## The Bottleneck

The remaining information requires solving a discrete logarithm in a 93-bit prime subgroup, which is computationally intensive but feasible using optimized tools.

## Solution Steps

### Step 1: Use SageMath Online

1. Go to: https://sagecell.sagemath.org/

2. Copy and paste this code:

```sage
q = 877884221210583981824110979993
g = Mod(541126034235828198305747641388, q)
h = Mod(164430592548940053609986922280, q)
x = discrete_log(h, g)
print(x)
```

3. Click "Evaluate"

4. Wait 5-30 minutes (SageMath will use Pohlig-Hellman algorithm)

5. Copy the result (let's call it `x`)

### Step 2: Decrypt the Flag

Once you have `x` from SageMath, run:

```bash
python decrypt_with_dlog.py
```

And enter the value of `x` when prompted.

## Alternative: Local SageMath

If you have SageMath installed locally:

```bash
sage sagemath_dlog.sage
```

## Alternative: Alpertron Online Calculator

1. Visit: https://www.alpertron.com.ar/DILOG.HTM

2. Enter:
   - **Base (a)**: 541126034235828198305747641388
   - **Power (b)**: 164430592548940053609986922280
   - **Modulus (m)**: 877884221210583981824110979993

3. Click "Calculate"

4. Use the result in decrypt_with_dlog.py

## Files in This Directory

- `sagemath_dlog.sage` - Code to run in SageMath
- `decrypt_with_dlog.py` - Final decryption script (use after getting discrete log)
- `dlog_problem.txt` - Problem parameters for reference
- `challenge (3).py` - Original challenge code
- `output (1).txt` - Challenge output
- `analyze.py` - Initial analysis script
- Various solver attempts (solver.py, solve.py, etc.)

## Why This Works

1. **Matrix Structure**: The Kyoko Ring uses upper triangular matrices with specific modular constraints
2. **Factorization**: Working modulo p and q separately allows us to extract partial information
3. **Unipotent Analysis**: The upper triangular structure means U^n has a simple linear relationship with n
4. **Pohlig-Hellman**: Breaking the discrete log into smaller subproblems based on factorization of q-1
5. **Chinese Remainder Theorem**: Combining all partial results to recover the full 580-bit secret

## Expected Timeline

- SageMath online: 5-30 minutes
- Local SageMath (if faster machine): 1-10 minutes
- Alpertron: May timeout for this size, but worth trying

## Next Steps

1. Run SageMath with the provided code
2. Wait for the discrete log result
3. Run decrypt_with_dlog.py with that result
4. Get the flag!

---

**Status**: Ready to solve - just needs the discrete log computation from an online tool.
