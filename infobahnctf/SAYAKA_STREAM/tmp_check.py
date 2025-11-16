import random
import sys
from pathlib import Path
root = Path(__file__).resolve().parent.parent
sys.path.append(str(root / 'SAYAKA_STREAM'))
import solve
rng = random.Random(123)
for _ in range(solve.WARMUP_CALLS):
    rng.getrandbits(5)
state = rng.getstate()
print('expected', solve.START_INDEX)
print('actual', state[1][-1])
