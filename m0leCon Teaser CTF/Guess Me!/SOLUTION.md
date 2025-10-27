# Guess Me! - Solution Analysis

## Challenge Overview
- 5 rounds, 16 attempts per round
- Key is SHA256(shuffled("m0leCon"))[:16] → 7! = 5040 possibilities
- Need to authenticate with: AD=b"pretty please", MSG=b"next round please"

## The Problem
With 16 attempts and 5040 keys:
- Chance per round: 16/5040 = 0.32%
- Chance all 5 rounds: (16/5040)^5 ≈ 3.3 × 10^-15 (impossible!)

## Possible Solutions

### 1. **Key Reuse Across Rounds**
If the server reuses the same permutation across rounds, you only need to find it once!
- Test this by capturing server responses and checking patterns

### 2. **Multi-Nonce Attack (Initially Suspected)**
Server accepts multiple nonces but requires ALL to decrypt correctly.
- NOT exploitable as initially thought

### 3. **Custom Crypto Weakness in _perm()**
The `_perm` function uses:
- Custom SBOX
- Bit permutation: `(idx * 7) % 128`
- 10 rounds

Potential weaknesses:
- Permutation might not be a good diffusion
- SBOX might have algebraic properties
- Could allow forgery without knowing key

### 4. **Timing/Side Channel**
Different error messages or timing might leak information about correct key.

### 5. **Probability Boost**
Maybe keys follow a pattern (e.g., alphabetically sorted more often).
Or maybe only SOME permutations are used (not all 5040).

## Recommended Next Steps

1. **Test if key persists across rounds**:
   - Try the SAME key in round 2 that you tried in round 1
   - If it ever succeeds, the server is reusing keys!

2. **Analyze _perm() for weaknesses**:
   - Look for fixed points
   - Check if bit permutation has cycles
   - Test if SBOX is invertible/has collisions

3. **Try all 5040 in order until one works**:
   - Reconnect on failure
   - Eventually you'll hit the right one in ≤16 tries by luck

4. **Look for unintended solutions**:
   - Empty nonce?
   - Zero tag?
   - Padding oracle?

## Current Status
Your attempts show all "Tag is invalid" which means:
- Tags are being checked correctly
- None of your guessed keys matched

The empty response in round 2 is suspicious and might indicate:
- You disconnected/server error
- OR you actually got it right but output was lost
