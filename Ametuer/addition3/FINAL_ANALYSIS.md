# addition3 - Final Analysis and Solution Strategy

## Challenge Code Review

```python
flag = bytes_to_long(flag) << 512  # Flag shifted left 512 bits
n = <2048-bit RSA modulus via openssl>
e = 3

while True:
    cs = [flag + getrandbits(512) for _ in range(100000)]
    scramble = int(input('scramble the flag: '))
    ms = [(m + scramble)%n for m in cs]
    c = choice([pow(m, e, n) for m in ms])
```

## The Critical Issue: Random Selection

The server creates 100,000 different plaintexts (each with a different 512-bit random mask) and then **randomly selects ONE** to encrypt and return.

This means:
- Even if our flag guess is perfect, only 1 out of 100,000 messages will produce a perfect cube
- The probability of getting the "perfect cube" message is 1/100,000 = 0.001%
- We need ~69,000 samples to have 50% chance of seeing one perfect cube
- With server rate limiting, this approach is impractical

## Why the Original Approach Fails

The solver I created assumes we can detect a perfect cube on a single query. But because of the `choice()` operation:

```python
# Even with perfect guess:
test_flag = actual_flag
scramble = -(test_flag << 512)

# ONE message will be: t = r (perfect cube when cubed)
# But 99,999 messages will be: t = r + k*n for different r values

# Server returns ONE random choice - likely NOT the perfect cube
```

## Alternative Attack Vectors

### Option 1: Statistical Sampling (IMPRACTICAL)
- Collect 500+ samples per guess
- Count perfect cubes (expect ~5 for correct, ~0 for wrong)
- **Problem:** Server rate limits after ~100 connections
- **Status:** Not feasible

### Option 2: Lattice/Coppersmith Attack
The plaintext has structure:
```
m = (flag << 512) + r + scramble (mod n)
c = m^3 (mod n)
```

With scramble = 0, we have:
```
m = F*2^512 + r (mod n)
m^3 ≡ c (mod n)
```

Where F (flag) is unknown but small (~416 bits), and r is unknown and small (~512 bits).

This is a **bivariate Coppersmith problem**:
- f(x, y) = (x*2^512 + y)^3 - c
- Find small roots where |x| < 2^416 and |y| < 2^512

**Challenges:**
- Need enough samples (different n values make this harder)
- Bivariate Coppersmith is less reliable than univariate
- May need SageMath/fpylll for implementation

### Option 3: Timing Side Channel (UNLIKELY)
If `choice()` and `pow()` take different times based on message structure, we might detect patterns. But this is unreliable over network.

### Option 4: Birthday Paradox on Random Masks
With 100,000 messages per query, there's a birthday paradox: some random masks might collide across queries. But with 512-bit values, collision probability is negligible.

## Recommended Solution: Lattice Attack

Given the constraints, the most practical approach is:

1. **Collect samples with scramble = 0:**
   ```bash
   python collect_samples.py  # Gather n, c pairs
   ```

2. **Use Coppersmith/LLL in SageMath:**
   ```python
   # For each (n, c) pair:
   PR = PolynomialRing(Zmod(n), names=('x', 'y'))
   x, y = PR.gens()
   f = (x * 2^512 + y)^3 - c

   # Find small roots
   roots = f.small_roots(X=2^420, Y=2^515, beta=1.0)
   ```

3. **Extract flag from recovered roots:**
   ```python
   if roots:
       flag_int, r = roots[0]
       flag = long_to_bytes(int(flag_int))
   ```

## Implementation Status

### What Works:
✓ Perfect cube detection logic (tested locally)
✓ Understanding of the vulnerability
✓ Server connection and protocol parsing

### What Doesn't Work:
✗ Single-query perfect cube detection (due to random selection)
✗ Statistical sampling (due to rate limiting)

### What Needs Implementation:
- Bivariate Coppersmith attack in SageMath
- Lattice reduction on collected samples
- Alternative: Try to find weakness in OpenSSL's RSA generation

## Files Created

1. **solve_final.py** - Single-query solver (doesn't work due to random selection)
2. **solve_statistical.py** - Multi-sample solver (rate limited)
3. **solve_debug.py** - Debug/testing script
4. **collect_samples.py** - Collects (n, c) pairs for lattice attack
5. **ddition3_lattice_attack.sage** - Starter SageMath script (needs expansion)

## Conclusion

The challenge is **harder than initially analyzed** due to the random selection of one message from 100,000. The perfect cube detection approach works in theory but is impractical due to:

1. Low probability (0.001% per query)
2. Server rate limiting
3. Need for 10,000+ queries per byte

The intended solution likely involves:
- **Coppersmith/lattice-based attack** on the polynomial structure
- OR **leveraging weaknesses in OpenSSL RSA generation** (deterministic patterns)
- OR **some other mathematical property** I haven't identified yet

Given the challenge had only 2 solves and 484 points, it's definitely a hard challenge requiring advanced techniques beyond simple cube root detection.

## Next Steps if Continuing

1. Implement proper bivariate Coppersmith in SageMath
2. Collect more samples with different scramble values
3. Research OpenSSL RSA generation for potential weaknesses
4. Look for patterns in the moduli across queries
5. Consider if there's a way to bias the `choice()` selection

The theoretical approach (perfect cube detection) is sound, but the practical implementation is blocked by the random selection mechanism.
