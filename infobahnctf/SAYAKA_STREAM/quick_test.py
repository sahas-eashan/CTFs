import random, sys
from pathlib import Path
root = Path(__file__).resolve().parent
sys.path.append(str(root))
from solve import recover_state, coords_for_prefix, WARMUP_CALLS

def sayaka_bit(rng):
    x = rng.getrandbits(5)
    a,b,c,d,e = [(x>>i)&1 for i in range(5)]
    return int((a or not b or c==d or d!=e) and (not a or b or c or d or not e))

rng = random.Random(12345)
for _ in range(WARMUP_CALLS):
    rng.getrandbits(5)
TOTAL = 42**3
bits = [sayaka_bit(rng) for _ in range(TOTAL)]
obs_len = 500
obs = bits[:obs_len]
coords = coords_for_prefix(obs_len)
state, rx, ry, rz = recover_state(obs, coords)
print('solved')
