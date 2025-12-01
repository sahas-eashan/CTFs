#!/usr/bin/env python3
from z3 import *

# 1. Setup the solver and 43 flag variables (as 8-bit bytes)
s = Solver()
flag = [BitVec(f'flag_{i}', 8) for i in range(43)]

# 2. Add constraint: all flag characters must be printable ASCII
for char in flag:
    s.add(And(char >= 32, char <= 126))

# 3. Read the module.wat file and simulate the stack machine
stack = []
with open('module.wat') as f:
    for line in f:
        parts = line.strip().split(' ')
        op = parts[0]

        try:
            if op == "i32.const":
                stack.append(int(parts[1]))
            elif op == "i32.load8_u":
                addr = stack.pop()
                stack.append(flag[addr])
            elif op == "i32.add":
                b = stack.pop()
                a = stack.pop()
                stack.append(a + b)
            elif op == "i32.sub":
                b = stack.pop()
                a = stack.pop()
                stack.append(a - b)
            elif op == "i32.mul":
                b = stack.pop()
                a = stack.pop()
                stack.append(a * b)
            elif op == "i32.xor":
                b = stack.pop()
                a = stack.pop()
                stack.append(a ^ b)
            elif op == "i32.and":
                b = stack.pop()
                a = stack.pop()
                stack.append(a & b)
            elif op == "i32.or":
                b = stack.pop()
                a = stack.pop()
                stack.append(a | b)
            elif op == "i32.ne":
                # This is the key! The code checks if (calc != expected).
                # We add a constraint that they MUST be equal.
                expected_val = stack.pop()
                calculated_val = stack.pop()
                s.add(calculated_val == expected_val)
        except Exception as e:
            print(f"Error processing line: {line.strip()} -> {e}")
            pass

# 4. Solve and print the flag
if s.check() == sat:
    print("Solver found a solution!")
    m = s.model()
    result = bytearray(43)
    for i in range(43):
        result[i] = m[flag[i]].as_long()
    print(f"Flag: {result.decode('ascii')}")
else:
    print("Solver could not find a solution (unsatisfiable).")
