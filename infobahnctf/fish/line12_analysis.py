# What if line 12 creates a value like: 10*3+10*6+10*6+10*6 = 30+60+60+60 = 210?
# No, that's not ASCII...

# Let me re-trace: a*3+a*6+a*6+a*6++
# Assuming stack has value V from previous lines:
# a -> push 10
# * -> multiply: V*10
# 3 -> push 3
# + -> add: V*10 + 3
# a -> push 10
# * -> multiply: (V*10+3) * 10
# 6 -> push 6
# + -> add: (V*10+3)*10 + 6
# a -> push 10
# * -> multiply: ((V*10+3)*10 + 6) * 10
# 6 -> push 6
# + -> add: ((V*10+3)*10 + 6)*10 + 6
# + -> NOW THIS IS THE PROBLEM - what does ++ do?
#
# If stack is [X], then + might error OR...
# Wait! What if the PREVIOUS line left TWO values on the stack?

# Let me re-look at the structure. Lines 7-11 might work TOGETHER!

# Line 7 builds cumulative, then goes down (v)
# Line 8 continues building (reading RIGHT TO LEFT), then goes left (<)
# Line 9 continues, goes down (v)
# Line 10 continues (right to left), goes left (<)
# Then line 12 finishes and outputs!

# So the FINAL cumulative value from all 4 lines is:
#   132453609765128534888987732389980753698816
# Then line 12 does: a*3+a*6+a*6+a*6++
# Which means: (final_value * 10 + 3) * 10 + 6...

final = int("132453609765128534888987732389980753698816")

# Apply line 12: a*3+a*6+a*6+a*6
val = final
val = val * 10 + 3
val = val * 10 + 6
val = val * 10 + 6
val = val * 10 + 6

print(f"After a*3+a*6+a*6+a*6: {val}")

# Now the ++ ... what if it adds TWO separate things?
# Or duplicates and adds?  val + val = 2*val?

val2 = val + val
print(f"If ++ means add to self: {val2}")

# Now apply the output formula: (val % 96) + 32
result1 = (val % 96) + 32
result2 = (val2 % 96) + 32

print(f"\nWith val: ({val} % 96) + 32 = {result1} = '{chr(result1) if 32 <= result1 < 128 else '???'}'")
print(f"With val*2: ({val2} % 96) + 32 = {result2} = '{chr(result2) if 32 <= result2 < 128 else '???'}'")
