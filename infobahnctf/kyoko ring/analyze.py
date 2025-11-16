from math import gcd
from functools import reduce
from collections import Counter
import ast


with open(
    r"c:\Users\Cyborg\Documents\GitHub\CTFs\infobahnctf\kyoko ring\output (1).txt",
    "r",
) as fh:
    lines = [line.strip() for line in fh.readlines() if line.strip()]

if len(lines) != 3:
    raise SystemExit(
        f"Unexpected output format with {len(lines)} non-empty lines: {lines[:3]}..."
    )

g = ast.literal_eval(lines[0])
gs = ast.literal_eval(lines[1])
cipher_hex = lines[2]

vals_g = [int(x) for row in g for x in row]

c = Counter()
for idx, a in enumerate(vals_g):
    for b in vals_g[idx + 1 :]:
        g2 = gcd(a, b)
        if g2 > 1:
            c[g2] += 1

print("Top gcds among g entries:")
for k, v in c.most_common(10):
    print(k, v)

p_candidates = [g[1][0], g[2][0], g[2][1]]
q_candidates = [g[0][1], g[0][2], g[1][2]]


def gcd_list(lst):
    return reduce(gcd, [abs(int(x)) for x in lst])


p = gcd_list(p_candidates)
q = gcd_list(q_candidates)

print("p candidate:", p)
print("q candidate:", q)

print("Sanity gcd g[0][0], g[1][1] =", gcd(int(g[0][0]), int(g[1][1])))
print("Ciphertext:", cipher_hex)

diag_gcds = [gcd(int(gs[i][i]), int(g[i][i])) for i in range(3)]
print("Diagonal gcds between g**secret and g:", diag_gcds)
