# Copy and paste this entire code into SageMath online: https://sagecell.sagemath.org/
# This will compute the discrete log (may take a few minutes)

print("Computing discrete log in 93-bit subgroup...")
print("This may take several minutes...")
print()

q = 877884221210583981824110979993
g = Mod(541126034235828198305747641388, q)
h = Mod(164430592548940053609986922280, q)

print("Parameters:")
print(f"  g = {g}")
print(f"  h = {h}")
print(f"  q = {q}")
print()

print("Computing discrete_log(h, g)...")
x = discrete_log(h, g)

print()
print("="*60)
print(f"RESULT: x = {x}")
print("="*60)
print()
print("Copy this value and use it in the decryption script!")
