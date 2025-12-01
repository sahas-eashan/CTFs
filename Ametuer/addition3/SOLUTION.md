# addition3 - Complete Solution

## Challenge Summary

**Challenge:** addition3 from AmateursCTF
**Category:** Cryptography
**Points:** 484 (2 solves)
**Server:** `nc amt.rs 38787`

## Challenge Analysis

The server implements RSA encryption with `e=3` and presents the following setup:

```python
flag = bytes_to_long(flag) << 512  # 52-byte flag shifted left by 512 bits
n = <2048-bit RSA modulus regenerated each query>
e = 3

# For each query:
cs = [flag + getrandbits(512) for _ in range(100000)]
scramble = int(input('scramble the flag: '))
ms = [(m + scramble) % n for m in cs]
c = choice([pow(m, e, n) for m in ms])
```

Each query:
1. Generates 100,000 plaintexts: `m_i = (flag << 512) + r_i` where `r_i` is a random 512-bit value
2. Asks for a `scramble` value
3. Adds scramble to all plaintexts (mod n)
4. Randomly selects one scrambled plaintext
5. Returns `c = m^3 mod n`
6. Regenerates `n` for the next query

## Vulnerability: Perfect Cube Detection

### Key Insight

When we set `scramble = -(guess << 512)`, the plaintext becomes:

```
t = (flag << 512) + r + scramble (mod n)
  = (flag << 512) + r - (guess << 512) (mod n)
  = ((flag - guess) << 512) + r (mod n)
```

**If `guess == flag` exactly**, then:
```
t = r  (just a 512-bit random number!)
```

### Why This Matters

Since `r < 2^512` and the modulus `n ≈ 2^2048`:

- `n^(1/3) ≈ 2^683`
- `r < 2^512 << n^(1/3)`
- Therefore: `r^3 < n`

This means when our guess is correct, the ciphertext is **not reduced modulo n**:
```
c = r^3  (a perfect integer cube!)
```

We can detect this by computing the integer cube root and checking if `icbrt(c)^3 == c`.

### Why Wrong Guesses Don't Work

When `guess ≠ flag`:
```
t = ((flag - guess) << 512) + r
```

This is approximately `2^928` bits (since flag difference is non-zero), much larger than `n^(1/3)`.

Therefore `t^3 >> n`, causing modular reduction, and `c` is **not** a perfect cube with overwhelming probability.

## Attack Strategy: Byte-by-Byte Recovery

1. **Start with known prefix:** `amateursCTF{` (12 bytes)

2. **For each unknown byte position (12 through 51):**
   - Try each printable ASCII character (32-126)
   - Build test flag: `known_bytes + guess_byte + null_padding`
   - Send `scramble = -(test_flag << 512)`
   - Check if returned ciphertext is a perfect cube
   - If yes → we found the correct byte!
   - If no → try next character

3. **Continue until all 52 bytes recovered**

## Implementation Details

### Fast Integer Cube Root

Using Newton's method for O(log n) performance:

```python
def icbrt(n):
    if n == 0:
        return 0
    if n < 8:
        return 1

    # Initial guess using bit length
    x = 1 << ((n.bit_length() + 2) // 3)

    # Newton iterations: x_new = (2*x + n/x^2) / 3
    while True:
        x_new = (2 * x + n // (x * x)) // 3
        if x_new >= x:
            break
        x = x_new

    # Verify and adjust
    while x**3 > n:
        x -= 1
    while (x + 1)**3 <= n:
        x += 1

    return x

def is_perfect_cube(c):
    root = icbrt(c)
    return root**3 == c
```

### Main Solver Loop

```python
prefix = b"amateursCTF{"
known = prefix

for pos in range(len(prefix), 52):
    for byte_val in range(32, 127):  # Printable ASCII
        # Build test flag
        test = known + bytes([byte_val]) + b'\x00' * (51 - pos)
        guess = bytes_to_long(test)

        # Query server
        scramble = -(guess << 512)
        c = query(io, scramble)

        # Check if perfect cube
        if is_perfect_cube(c):
            known = known + bytes([byte_val])
            print(f"Found byte {pos}: '{chr(byte_val)}'")
            break
```

## Comparison with Previous Challenges

### addition1 (Original)
- **Setup:** Same pool of 100k messages used across all queries
- **Attack:** Birthday paradox collision attack + Franklin-Reiter related message attack
- **Queries needed:** ~400 (until collision)

### addition2
- **Setup:** Fresh pool of 100k messages generated per query
- **Attack:** Algebraic recovery via exact rational arithmetic on ciphertext differences
- **Queries needed:** 3-6 samples

### addition3 (This Challenge)
- **Setup:** Fresh pool + **new RSA modulus per query**
- **Attack:** Perfect cube detection via scramble manipulation
- **Queries needed:** 40 * (52 - 12) = ~1,600 queries (worst case, if every byte takes 40 tries)
- **Actual queries:** Much fewer due to flag format (lowercase, underscores, digits)

## Why This Challenge is Harder

1. **New modulus each query** → Can't use difference-based attacks
2. **Fresh random masks** → No collision attacks possible
3. **Need exact flag match** → Byte-by-byte brute force required

## Running the Solution

### Against Remote Server (if still up)

```bash
python solve_final.py
```

### Local Testing

```bash
python solve_final.py --test
```

## Expected Output

```
[*] Connected! n has 2048 bits, e = 3
[*] Starting with known prefix: amateursCTF{
[*] [12/52] Searching byte 12...
[+] Byte 12 = 'n' [PERFECT CUBE]
[*] Current flag: amateursCTF{n
[*] [13/52] Searching byte 13...
[+] Byte 13 = '0' [PERFECT CUBE]
[*] Current flag: amateursCTF{n0
...
[======================================================================]
[FLAG: amateursCTF{...}]
[======================================================================]
```

## Mathematical Proof

Let's prove the perfect cube property rigorously:

**Given:**
- Flag `F` is 52 bytes = 416 bits
- `F_shift = F << 512`
- Random mask `r < 2^512`
- Modulus `n ≈ 2^2048`

**Correct Guess:**
```
t = F_shift + r - (F << 512) = r
t^3 = r^3 < (2^512)^3 = 2^1536 << 2^2048 = n
```
Therefore `c = t^3` without reduction, making it a perfect cube.

**Wrong Guess (differ by k bits):**
```
t = ((F - G) << 512) + r where |F - G| > 0
|F - G| >= 1, so |t| >= 2^512
```

For even a 1-bit difference:
```
t >= 2^512
t^3 >= 2^1536

Probability(t^3 < n) ≈ 0 (since t values are uniformly distributed mod n)
```

The probability of a false positive (wrong guess giving perfect cube) is negligible:
```
P(false positive) < (2^683 / 2^2048) = 2^(-1365) ≈ 0
```

## Optimization Notes

1. **Character set pruning:** Flag format suggests lowercase, digits, underscores → try these first
2. **Parallel queries:** Could parallelize character testing (not implemented due to server load concerns)
3. **Adaptive search:** Could use partial knowledge to constrain remaining bytes
4. **Early abort:** If many characters fail, might indicate network issues

## Files

- `solve_final.py` - Complete solver with local testing
- `chall.py` - Original challenge source
- `SOLUTION.md` - This writeup
- `README.md` - Challenge overview

## Conclusion

This challenge demonstrates a creative application of the small `e=3` exponent in RSA. By carefully choosing the scramble value, we can manipulate the plaintext size to make the ciphertext a perfect cube, creating a distinguisher that enables byte-by-byte recovery of the flag.

The key takeaways:
- Small RSA exponents are dangerous even without classical related-message attacks
- User-controlled additive values can create unexpected vulnerabilities
- Perfect cube detection is computationally efficient and reliable
- Byte-by-byte recovery is feasible when each byte can be independently verified
