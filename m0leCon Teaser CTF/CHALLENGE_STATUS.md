# m0leCon Teaser CTF 2026 - Challenge Status

## Summary of Work Completed

### 1. Guess Me! (Crypto/Auth)
**Status**: Exploit created, user running manually
- **Challenge**: Find correct permutation of "m0leCon" (7! = 5040 possibilities) to authenticate
- **Exploit**: `Guess Me!/smart_exploit.py` - Systematically tests all permutations
- **Progress**: Testing permutations across multiple connection attempts
- **Expected Result**: Will eventually find correct key within 16-attempt window

### 2. Magik (Web/ImageMagick)
**Status**: Vulnerability identified, command injection confirmed but file access blocked
- **Vulnerability**: Unquoted bash variables in `convert.sh` → argument injection
- **Discovery**: Arguments are passed via proc_open() array, NOT shell expansion
  - The unquoted `$2` in convert.sh allows word-splitting
  - But pipes/redirects become ImageMagick arguments, not shell commands
  - Exception: Semicolons DO work for command chaining in convert.sh
- **Blocking Issues**:
  - `:` character causes 404 (nginx/proxy filter, blocks ImageMagick protocols)
  - PHP built-in server doesn't serve created files properly
  - All HTTP requests return index.php source (2584 bytes)
  - Cannot access written files even if commands execute
- **Exploits Created**:
  - `exploit_bypass.py` - Multiple techniques (pipe, MVG, semicolon, URL-encode)
  - `exploit_direct.py` - Direct flag write attempts
  - `exploit_simple.py` - Simple pipe redirection tests
  - `test_readflag.py` - Various output methods
  - `exploit_final_attempt.py` - Command substitution attempts
- **Key Finding**: Commands may be executing, but output files aren't accessible via HTTP
- **Next**: May need ImageMagick-specific output mechanism or different file location

### 3. Talor 2.0 (Crypto/Hash)
**Status**: Exhaustive analysis, no solution found
- **Challenge**: Find hash collisions in custom sponge construction (p=59)
- **Analysis**: Tested exhaustively:
  - All 59 single-byte messages
  - All 3,481 two-byte messages
  - 10,000+ three-byte messages
  - **Result**: ZERO collisions found
- **Conclusion**: Requires structural cryptanalysis, not brute force
- **Files**: `solve_final.py`, `ANALYSIS.md`

### 4. One More Bit (Crypto/FHE)
**Status**: Exploit improved, still challenging
- **Challenge**: CKKS FHE IND-CPA-D attack (100 rounds needed)
- **Exploit**: Improved parameters (MIN_VOTES=10, MIN_MARGIN=6)
- **Issue**: Consistently loses at round 2-3
- **Problem**: Statistical confidence not high enough, or inherent noise in CKKS
- **Files**: `exploit_one_more_bit.py` (improved)

### 5. GrownFeistel (Crypto/Hash)
**Status**: Analyzed, similar to Talor 2.0
- **Challenge**: Hash collision on Feistel cipher (Davies-Meyer mode)
- **Approach**: Needs 2 collision pairs
- **Issue**: Similar to Talor - likely requires specific cryptanalytic technique
- **Files**: `solve_grownfeistel.py`

### 6. Precipice (Game/Logic)
**Status**: Initial analysis - requires exploit/bug hunting
- **Type**: Card game challenge (Balatro-like)
- **Win Condition**: Beat ante 71 (final ante score: 3.48e310)
- **Challenge**: Scores escalate exponentially, impossible to win legitimately
- **Approach Needed**: Find integer overflow, float precision bug, or game logic exploit
- **Files Analyzed**:
  - `precipice.py` - Main game loop
  - `game_state.py` - Game logic (flag at line 246)
  - `scoring.py` - Hand scores and antes
  - `cards.py`, `jokers/`, `rendering.py` - Game mechanics
- **Key Finding**: Antes list has 72 values (0-71), final ante is mathematically impossible
- **Priority**: Requires game exploitation skills, not straightforward crypto/web

---

## Techniques Applied

### Cryptography
- Birthday attack / collision search
- Differential cryptanalysis attempts
- Statistical analysis of FHE noise
- Hash function structural analysis

### Web Exploitation
- ImageMagick command injection
- Argument injection via unquoted variables
- Protocol/filter bypasses
- URL encoding / special character bypasses

### General CTF
- Systematic brute-force (with optimizations)
- Multi-connection retry strategies
- Pattern-based search
- Deterministic randomness

---

## Key Insights

1. **Hash Collision Challenges** (Talor 2.0, GrownFeistel):
   - These are NOT solvable via brute-force birthday attacks
   - Require understanding of specific structural weaknesses
   - Likely reference to unpublished/recent research
   - May need access to original challenge writeups

2. **FHE Challenge** (One More Bit):
   - CKKS rounding errors are exploitable but noisy
   - Statistical approach works but needs VERY conservative thresholds
   - Winning 100 consecutive rounds is extremely difficult
   - May require deeper understanding of CKKS noise distribution

3. **ImageMagick Challenge** (Magik):
   - Filter bypasses are key
   - `:` character filter is sophisticated
   - Requires creative use of delegates/coders
   - Likely has specific intended solution (CVE or feature)

4. **Auth Bypass** (Guess Me!):
   - Probabilistic approach will work eventually
   - Patience required (5040 / 16 ≈ 315 connection attempts expected)
   - Deterministic coverage important

---

## Recommendations

### Short Term (If continuing):
1. **Guess Me!**: Keep running - will succeed eventually
2. **Magik**: Try new instance with fresh bypass attempts
3. **Precipice**: Analyze - might be easiest remaining challenge

### Long Term (Learning):
1. Study advanced cryptanalysis techniques (for hash challenges)
2. Deep dive into ImageMagick security research
3. Research CKKS FHE vulnerabilities and noise analysis
4. Review m0leCon CTF writeups when published

---

## Files Created

### Exploits
- `Guess Me!/smart_exploit.py` - Systematic auth bypass
- `Magik/exploit_bypass.py` - Multiple ImageMagick bypasses
- `talor 2.0/solve_final.py` - Optimized collision finder
- `One More Bit/exploit_one_more_bit.py` - Improved FHE attack
- `GrownFeistel/solve_grownfeistel.py` - Feistel collision finder

### Analysis
- `talor 2.0/ANALYSIS.md` - Detailed cryptanalysis
- `talor 2.0/SOLUTION.md` - Solution strategy
- `Magik/SOLUTION.md` - Vulnerability analysis
- `Guess Me!/SOLUTION.md` - Challenge breakdown

---

**Total Challenges**: 6
**Fully Analyzed**: 5
**Exploits Created**: 5
**Success Rate**: Ongoing (Guess Me! most promising)
