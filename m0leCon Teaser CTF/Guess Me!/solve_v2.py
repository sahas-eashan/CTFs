#!/usr/bin/env python3
"""
Guess Me! Exploit - Correct Strategy

The vulnerability: Server accepts MULTIPLE nonces and checks if ANY decrypt successfully.

Key insight: We need to create a (ciphertext, tag) pair that is valid for
MULTIPLE (key, nonce) combinations!

Actually, better insight: The PRF uses AES(key, SHA256(block_index)) as the mask.
If we can find a collision or pattern, we might be able to reuse keystreams.

Simpler approach: Since server tries ALL our nonces with ITS key, we need to:
1. Generate (nonce_i, ct, tag) for each possible key_i
2. Send ALL nonces at once
3. ONE of them will match the server's key!

But we can only send ONE ciphertext and ONE tag...
So we need ct and tag that work with (server_key, one_of_our_nonces)

Let me think differently:
- For a FIXED plaintext and FIXED additional_data
- Generate encryptions with ALL 5040 different keys
- Use a DIFFERENT nonce for each key
- Send all 5040 nonces
- Send ONE ciphertext (encrypted with one of the keys)
- The server will try OUR ciphertext with ALL our nonces using ITS key
- ONE (nonce, server_key) combination should produce the same keystream as our (nonce, our_key)!

No wait, that's not right either...

Let me re-read the code more carefully...

Actually, the issue is we need KEYSTREAM COLLISION.
keystream_i = _prf(idx, key_i, nonce_i)

If we can find two combinations where:
_prf(0, key_server, nonce_x) == _prf(0, key_attacker, nonce_attacker)

Then our ciphertext will decrypt correctly!

This is VERY hard... unless there's a weakness in _prf.

Alternative: What if we can forge a valid tag without knowing the key?
Or what if there's a collision in the permutation function?

Let me look at _prf more carefully:
mask = AES.encrypt(SHA256(block_index))
result = XOR(data, mask[:16])
result = _perm(result)  # 10 rounds of SBOX + bit permutation
result = XOR(result, mask[16:32])

Hmm, this is a custom construction. Let me think about attacks...

WAIT! I just realized something. Let me check the code again...

Looking at line 118: nonces = [nonces[i:i+BLOCK_SIZE] for i in range(0, len(nonces), BLOCK_SIZE)]

We can send MULTIPLE 16-byte nonces! And the server will try to decrypt with EACH ONE!

So the strategy is:
1. Pick a fixed random nonce N1
2. Encrypt "next round please" with each of the 5040 keys using nonce N1
3. This gives us 5040 different (ciphertext, tag) pairs
4. But we can only send ONE ciphertext and ONE tag...

Hmm, still doesn't work.

Unless... what if we send 5040 nonces, and for EACH key we use the SAME nonce?
Then we'd have 5040 identical nonces, which doesn't help.

Let me think about this from a different angle:

What if we PARTIALLY bruteforce? With 16 attempts and 5040 permutations:
- We can try 16 different keys per round
- Probability of success in one round: 16/5040 ≈ 0.32%
- Probability of failing all 5 rounds: (1-0.0032)^5 ≈ 98.4%

That's not good.

WAIT! Reading the code again at line 122-129:

```python
decs = [decrypt(key, nonce, ciphertext, additional_data, tag) for nonce in nonces]
auth = any(decs)
if auth:
    if additional_data != b"pretty please":
        ...
    else:
        if all([dec == b"next round please" for dec in decs]):
```

The condition is:
- ANY decryption succeeds (tag validates) → auth = True
- ALL successful decryptions must equal b"next round please"

So if we send 2 nonces:
- nonce1 with valid tag → decrypts to "next round please"
- nonce2 with invalid tag → returns False or "Invalid padding"

Then `any(decs)` is True (because nonce1 worked)
And we need `all([dec == b"next round please" for dec in decs])`

If decs = [b"next round please", False], then all([...]) checks if False == b"next round please", which fails!

So ALL our nonces must produce valid decryptions!

That means we need to send multiple nonces that ALL decrypt to the same message with the server's key.

This is only possible if we KNOW the server's key... which defeats the purpose.

UNLESS... there's a different vulnerability I'm missing.

Let me look for weaknesses in the _pad_pkcs7 or _perm functions...
