# pwn.red Proof-of-Work Algorithm Explanation

## Summary

The pwn.red PoW system uses **modular exponentiation**, NOT SHA256 or other hash-based algorithms!

## Challenge Format

```
s.BASE64(difficulty).BASE64(challenge)
```

Example: `s.AAAACg==.3wo2Hapx80nWQ0eheMAE/A==`

- Part 1: `s` (version identifier)
- Part 2: `AAAACg==` (base64-encoded difficulty = 10)
- Part 3: `3wo2Hapx80nWQ0eheMAE/A==` (base64-encoded challenge bytes)

## Solution Format

```
s.BASE64(solution)
```

Example: `s.LeDtYaXfoW9v0YKNJTE//TkGJUQILxP2Th9bJoluFWEn9k+LbD8zkCBqnyr1z0z2TA18GZW65OwZ4/dhri3rCvT+zaBzgD+4yKoRypaL1PS79Kd8t0hPXpUYrHx4zFTx/6NNlRgWsWGEYQY4MmAKNHJen4IoMTU8+v+MvEDJyttfd24BWr7rucqBI7QUZW70bGfBdAVnqSdZkGWEFjoBnA==`

- Part 1: `s` (version identifier)
- Part 2: Base64-encoded solution bytes

## Algorithm

### Constants (from redpwn/pow source code)

```python
mod = (2 ** 1279) - 1  # Modulus: 2^1279 - 1
exp = 2 ** 1277         # Exponent: 2^1277
```

### Solving Process

1. **Parse the challenge:**
   ```python
   difficulty = int.from_bytes(base64.b64decode(difficulty_b64), 'big')
   x = int.from_bytes(base64.b64decode(challenge_b64), 'big')
   ```

2. **Perform modular exponentiation with XOR:**
   ```python
   for i in range(difficulty):
       x = pow(x, exp, mod)  # x^exp mod mod
       x ^= 1                 # XOR with 1
   ```

3. **Encode the solution:**
   ```python
   solution_bytes = x.to_bytes((x.bit_length() + 7) // 8, 'big')
   solution = f"s.{base64.b64encode(solution_bytes).decode('ascii')}"
   ```

## Why Your SHA256 Approach Failed

The common mistake is to assume pwn.red uses a hash-based PoW like hashcash:
```python
# WRONG APPROACH - This is NOT how pwn.red works!
hash_result = hashlib.sha256(challenge_bytes + nonce_bytes).digest()
# Check for leading zero bits...
```

pwn.red uses a **non-parallelizable** modular exponentiation algorithm instead, which:
- Cannot be easily parallelized across multiple cores
- Has predictable computation time based on difficulty
- Is verified by reversing the computation

## Verification Process (Server-Side)

The server verifies by reversing the computation:

```python
y = solution_value
for i in range(difficulty):
    y ^= 1           # XOR with 1
    y = y * y % mod  # Square (reverse of taking exp-th power)

# Check if y matches original challenge (or its negative)
```

## Performance Characteristics

From the redpwn/pow documentation:
- Each difficulty increase of **1500** requires approximately **1 second** of CPU time on a modern processor
- Difficulty 10 ≈ 0.0067 seconds (nearly instant)
- Difficulty 1500 ≈ 1 second
- Difficulty 15000 ≈ 10 seconds

## References

- Official Repository: https://github.com/redpwn/pow
- Source Code: https://github.com/redpwn/pow/blob/master/pow.go
- Official Solver: `curl -sSfL https://pwn.red/pow | sh -s <challenge>`

## Python Implementation

See `pwn_red_pow_solver.py` for a standalone solver or `pwn_red_pow_exploit.py` for integration with pwntools.

Key points for Python implementation:
1. Use Python's built-in `pow(base, exp, mod)` for efficient modular exponentiation
2. Handle large integers (1279+ bits) - Python handles this natively
3. Proper byte encoding with big-endian byte order
4. Correct base64 encoding/decoding

## Common Pitfalls

1. **Wrong algorithm**: Using SHA256 instead of modular exponentiation
2. **Wrong format**: Encoding nonce instead of the computed solution value
3. **Wrong byte order**: Using little-endian instead of big-endian
4. **Wrong solution format**: Forgetting the version prefix `s.`
5. **Empty bytes**: Not handling x=0 case properly in `to_bytes()`
