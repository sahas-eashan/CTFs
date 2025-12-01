# addition3 - AmateursCTF Crypto Challenge

## Challenge Description

```
crypto/addition 3
2 solves / 484 points
helloperson
now it does more prime generation
nc amt.rs 38787
```

## Solution Overview

The server encrypts messages using RSA with e=3:
- Plaintext structure: `m = (flag << 512) + random_512_bits + scramble (mod n)`
- Flag is 52 bytes, shifted left by 512 bits
- Random 512-bit mask `r` is added
- User supplies `scramble` value
- Server returns `c = m^3 mod n`

### Attack Strategy

When we set `scramble = -(guess << 512)`, the plaintext becomes:
```
t = (flag << 512) + r - (guess << 512) mod n
  = ((flag - guess) << 512) + r mod n
```

If `guess == flag` exactly, then `t = r`, which is just a 512-bit random number.

Since `r < 2^512` and `n^(1/3) ≈ 2^683`, we have `t^3 < n`, making `c = t^3` a **perfect integer cube**!

We can detect this by computing `icbrt(c)` and checking if `icbrt(c)^3 == c`.

### Byte-by-Byte Recovery

1. Start with known prefix: `amateursCTF{`
2. For each unknown byte position:
   - Try each printable ASCII character
   - Build test flag with current byte guess + null padding
   - Send `scramble = -(test_flag << 512)`
   - Check if returned ciphertext is a perfect cube
   - If yes, we've found the correct byte!
3. Continue until all 52 bytes recovered

## Files

- `chall.py` - Challenge source code
- `solve_addition3.py` - Automated solver script
- `README.md` - This file
- `NOTES.md` - Analysis notes

## Usage

### Solve Remote Challenge

```bash
python solve_addition3.py
```

### Test Locally

```bash
python solve_addition3.py --test
```

## Dependencies

```bash
pip install pycryptodome pwntools
```

## Flag Format

```
amateursCTF{...}
```

52 bytes total, standard flag format.
