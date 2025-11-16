# Re-parse line 12 more carefully
# >a*3+a*6+a*6+a*6++>:f1+6*%84*+o0$v
#
# a = 10
# * = multiply
# + = add
# : = duplicate
# f = 15
# % = modulo
# o = output
# $ = pop
# v = direction down

# Let's trace this: starting with stack value V (from previous lines)
# a      -> push 10, stack: [V, 10]
# *      -> multiply, stack: [V*10]
# 3      -> push 3, stack: [V*10, 3]
# +      -> add, stack: [V*10+3]
# a      -> push 10, stack: [V*10+3, 10]
# *      -> multiply, stack: [(V*10+3)*10]
# 6      -> push 6, stack: [(V*10+3)*10, 6]
# +      -> add, stack: [(V*10+3)*10+6]
# a      -> push 10, stack: [(V*10+3)*10+6, 10]
# *      -> multiply, stack: [((V*10+3)*10+6)*10]
# 6      -> push 6, stack: [((V*10+3)*10+6)*10, 6]
# +      -> add, stack: [((V*10+3)*10+6)*10+6]
# +      -> ADD AGAIN - but there's only one value on stack!
#          This means it adds the TOP with SECOND (if exists) or with itself
#          If stack has [X], then + makes [X+X] = [2*X]?
#
# Wait, no - in ><>, + needs TWO values. If there's only one, it might error
# OR the `++` is building from MULTIPLE VALUES from line 10!

# Let me reconsider... Maybe line 10 pushes MULTIPLE values onto stack?

# Line 10: v+0*a+7*a+5*a+3*a+6*a+9*a+8*a+8*a+1*a+6*a+10<
# Reading RIGHT to LEFT (because of the <):
# 10, a, 6, +, a, 1, +, a, 8, +, a, 8, +, a, 9, +, a, 6, +, a, 3, +, a, 5, +, a, 7, +, a, 0, +

print("Tracing line 10 (RIGHT TO LEFT due to <):")
print(
    "10, a, 6, +, a, 1, +, a, 8, +, a, 8, +, a, 9, +, a, 6, +, a, 3, +, a, 5, +, a, 7, +, a, 0, +"
)
print()

# Starting with stack from previous line (which has cumulative value)
# Let's assume it's empty for now
stack = []
stack.append(10)
print(f"10 -> {stack}")
stack.append(10)  # a
print(f"a -> {stack}")
b = stack.pop()
a = stack.pop()
stack.append(a * b)
print(f"* -> {stack}")
stack.append(6)
print(f"6 -> {stack}")
b = stack.pop()
a = stack.pop()
stack.append(a + b)
print(f"+ -> {stack}")
stack.append(10)  # a
print(f"a -> {stack}")
b = stack.pop()
a = stack.pop()
stack.append(a * b)
print(f"* -> {stack}")
stack.append(1)
print(f"1 -> {stack}")
b = stack.pop()
a = stack.pop()
stack.append(a + b)
print(f"+ -> {stack}")

print(f"\nPattern: 10*10+6 = {10*10+6}, then *10+1 = {(10*10+6)*10+1}")
print("This builds: 106, 1061...")
print()
print("OH! Each line doesn't build a cumulative - it might push SEPARATE values!")
