# addition3_lattice_attack.sage
samples = []
with open("samples.txt") as f:
    lines = f.read().split("\n")
    for i in range(0, len(lines), 4):
        if i+2 < len(lines):
            n = Integer(lines[i].split("=")[1].strip())
            e = Integer(lines[i+1].split("=")[1].strip())
            c = Integer(lines[i+2].split("=")[1].strip())
            samples.append((n, e, c))

n, e, _ = samples[0]
print("n =", n)
print("e =", e)

PR = PolynomialRing(Zmod(n), 'x')
x = PR.gen()

for idx, (_, _, c) in enumerate(samples):
    f = x^3 - c
    roots = f.small_roots(X=2^512, beta=1, epsilon=0.1)
    if roots:
        print(f"Sample {idx}: Found small root r = {roots[0]}")
        # You can now try to recover flag from m = r + (flag << 512)

print("If you need a more advanced lattice, let me know!")