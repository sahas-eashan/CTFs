from fish import Interpreter
import sys

code = open("chall.txt").read()
interp = Interpreter(code, "")  # NO INPUT

try:
    output = interp.execute()
    print("Output:", output)
except Exception as e:
    print(f"Error: {e}")
