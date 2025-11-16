import pathlib

code = pathlib.Path("chall.txt").read_text()
lines = code.split("\n")

# Let me re-examine the sequences more carefully
# Line 7: >~01+a*3+a*2+a*4+a*5+a*3+a*6+a*0+a*9+a*7+a*6v
# Line 8: v*a+8*a+8*a*8*a+4*a+3*a+5*a+8*a+2*a+1*a+5*a+<
# Line 9: >9+a*8+a*7+a*7+a*3+a*2+a*3+a*8+a*9+a*9+a*8+*v
# Line 10: v+0*a+7*a+5*a+3*a+6*a+9*a+8*a+8*a+1*a+6*a+10<
# Line 11: >a*3+a*6+a*6+a*6++>

print("Re-examining the code sequences:\n")
for i in range(7, 12):
    print(f"Line {i}: {lines[i]}")
print()

# Wait - maybe the digits aren't being used to BUILD numbers
# Maybe each digit is directly converted?
# Let me extract JUST the digits that appear after each operation

print("Extracting just the digit values added:\n")

# Line 7: 01+a*3+a*2+a*4+a*5+a*3+a*6+a*0+a*9+a*7+a*6
# Reading: 0, 1, (multiply by a=10), 3, (multiply by a), 2, ...
# Actually the operations are: 0 1 + a * 3 + a * 2 + ...
# Which in stack terms: push 0, push 1, add (=1), push 10, multiply (=10), push 3, add (=13)

# So each sequence builds ONE cumulative number
# But maybe I need to look at WHICH numbers are actually used in the output

# Looking at line 11-12 for the output routine:
# Line 11: >a*3+a*6+a*6+a*6++>:f1+6*%84*+o0$v
# This ALSO builds numbers first: 10*3=30, 30+10*6=90...
# Then >: duplicates, f1+6*% = (15+1)*6=96 modulo, 84* = 32 add, o = output

# But what VALUES are being output? Let me trace more carefully

# Actually looking at line 11-13:
# Line 11: >a*3+a*6+a*6+a*6++>:f1+6*%84*+o0$v
# Line 12:           vv?(0-1: ~v?)0+1:-*+f16<
# Line 13:            ;        >        $1+$^

# This is a LOOP that outputs characters!
# It takes values from the stack and outputs them one by one

# So the sequences in lines 7-10 push MULTIPLE values onto the stack
# Let me check: maybe each + operation pushes an intermediate result?

print("Maybe each intermediate value in the build is pushed?\n")


def trace_stack_operations(seq_str):
    """Trace what gets pushed to stack"""
    import re

    # Remove directional markers
    seq = (
        seq_str.replace("v", "")
        .replace(">", "")
        .replace("<", "")
        .replace("^", "")
        .replace("~", "")
    )

    stack = []
    current = 0

    tokens = re.findall(r"[0-9a-f]+|[+*]", seq.lower())

    i = 0
    while i < len(tokens):
        token = tokens[i]

        if token == "+":
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                current = a + b
                stack.append(current)
        elif token == "*":
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                current = a * b
                stack.append(current)
        else:
            val = int(token, 16)
            stack.append(val)

        i += 1

    return stack


for i in range(7, 12):
    seq = lines[i]
    stack = trace_stack_operations(seq)
    print(f"Line {i} final stack: {stack}")
    if stack:
        # Try converting last value with formula
        val = stack[-1]
        ascii_val = (val % 96) + 32
        if 32 <= ascii_val < 128:
            print(
                f"  Last value {val} -> (% 96) + 32 = {ascii_val} = '{chr(ascii_val)}'"
            )
