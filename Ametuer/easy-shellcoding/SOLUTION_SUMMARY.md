# pwn.red Proof-of-Work Solution Summary

## The Problem

You were trying to solve pwn.red PoW challenges using SHA256-based approach:
```python
# WRONG - This doesn't work!
hash_result = hashlib.sha256(challenge_bytes + nonce_bytes).digest()
# Check for leading zero bits...
solution = base64.b64encode(nonce_bytes).decode()  # Wrong!
```

The server kept rejecting with "incorrect proof of work".

## The Root Cause

**pwn.red does NOT use SHA256!** It uses a non-parallelizable modular exponentiation algorithm.

## The Correct Algorithm

### Constants
```python
mod = (2 ** 1279) - 1  # Modulus
exp = 2 ** 1277         # Exponent
```

### Solving Process
```python
# 1. Parse challenge
difficulty = int.from_bytes(base64.b64decode(difficulty_b64), 'big')
x = int.from_bytes(base64.b64decode(challenge_b64), 'big')

# 2. Perform modular exponentiation
for i in range(difficulty):
    x = pow(x, exp, mod)  # x^exp mod mod
    x ^= 1                 # XOR with 1

# 3. Encode solution
solution_bytes = x.to_bytes((x.bit_length() + 7) // 8, 'big')
solution = f"s.{base64.b64encode(solution_bytes).decode()}"
```

## Key Differences from Your Approach

| Your Approach (Wrong) | Correct Approach |
|----------------------|------------------|
| SHA256 hashing | Modular exponentiation |
| Find nonce with zero bits | Compute x^exp mod mod |
| Encode the nonce | Encode the computed result |
| Solution: `base64(nonce)` | Solution: `s.base64(result)` |

## Files Created

1. **`pwn_red_pow_solver.py`** - Standalone solver
   ```bash
   python pwn_red_pow_solver.py "s.AAAACg==.3wo2Hapx80nWQ0eheMAE/A=="
   ```

2. **`pwn_red_pow_exploit.py`** - Full exploit with pwntools integration
   ```bash
   python pwn_red_pow_exploit.py
   ```

3. **`test_pow_solver.py`** - Verification test
   ```bash
   python test_pow_solver.py
   ```

4. **`PWN_RED_POW_EXPLAINED.md`** - Detailed explanation

## Example

**Challenge:**
```
s.AAAACg==.3wo2Hapx80nWQ0eheMAE/A==
```

**Correct Solution:**
```
s.LeDtYaXfoW9v0YKNJTE//TkGJUQILxP2Th9bJoluFWEn9k+LbD8zkCBqnyr1z0z2TA18GZW65OwZ4/dhri3rCvT+zaBzgD+4yKoRypaL1PS79Kd8t0hPXpUYrHx4zFTx/6NNlRgWsWGEYQY4MmAKNHJen4IoMTU8+v+MvEDJyttfd24BWr7rucqBI7QUZW70bGfBdAVnqSdZkGWEFjoBnA==
```

## Usage with pwntools

```python
from pwn_red_pow_exploit import solve_pwn_red_pow

# In your exploit
io = remote('amt.rs', 57207)
data = io.recvuntil(b'solution: ')

# Extract and solve
match = re.search(r's\.[A-Za-z0-9+/=]+\.[A-Za-z0-9+/=]+', data.decode())
challenge = match.group(0)
solution = solve_pwn_red_pow(challenge)

# Send solution
io.sendline(solution.encode())
```

## Performance

- Difficulty 10: ~instant
- Difficulty 1500: ~1 second
- Difficulty 15000: ~10 seconds

Each difficulty increase of 1500 ≈ 1 second CPU time.

## References

- GitHub: https://github.com/redpwn/pow
- Official solver: `curl -sSfL https://pwn.red/pow | sh -s <challenge>`

## Verification

The test script verifies the solution by reversing the computation:
```python
# Server-side verification
for i in range(difficulty):
    y ^= 1
    y = (y * y) % mod  # Square (reverse of exp)

# Should get back to original challenge
assert y == challenge_x or y == (mod - challenge_x)
```

Tested and verified working!
