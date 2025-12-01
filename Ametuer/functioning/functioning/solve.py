import json
from z3 import BitVec, BitVecVal, Solver, UGE, ULE, UDiv, URem, If, LShR, sat

WIDTH = 32
MASK = (1 << WIDTH) - 1
ZERO = BitVecVal(0, WIDTH)
ONE = BitVecVal(1, WIDTH)

with open('J_ast.json') as f:
    J_AST = json.load(f)

class Interpreter:
    def __init__(self, ast, length=48):
        self.ast = ast
        self.length = length
        self.solver = Solver()
        self.chars = [BitVec(f'c{i}', WIDTH) for i in range(length)]
        low = BitVecVal(32, WIDTH)
        high = BitVecVal(126, WIDTH)
        for ch in self.chars:
            self.solver.add(UGE(ch, low))
            self.solver.add(ULE(ch, high))

    def as_expr(self, val):
        if isinstance(val, int):
            return BitVecVal(val & MASK, WIDTH)
        return val

    def is_int(self, val):
        return isinstance(val, int)

    def add(self, x, y):
        if self.is_int(x) and self.is_int(y):
            return x + y
        return self.as_expr(x) + self.as_expr(y)

    def mul(self, x, y):
        if self.is_int(x) and self.is_int(y):
            return x * y
        return self.as_expr(x) * self.as_expr(y)

    def sub(self, x, y):
        if self.is_int(x) and self.is_int(y):
            return x - y
        return self.as_expr(x) - self.as_expr(y)

    def band(self, x, y):
        if self.is_int(x) and self.is_int(y):
            return x & y
        return self.as_expr(x) & self.as_expr(y)

    def wrap(self, val, bits):
        mask = (1 << bits) - 1
        if self.is_int(val):
            return val & mask
        return self.as_expr(val) & BitVecVal(mask, WIDTH)

    def ge(self, x, y):
        if self.is_int(x) and self.is_int(y):
            return x >= y
        return UGE(self.as_expr(x), self.as_expr(y))

    def shr8(self, val):
        if self.is_int(val):
            return val >> 8
        return LShR(self.as_expr(val), 8)

    def div(self, x, y):
        if self.is_int(x) and self.is_int(y):
            return x // y
        return UDiv(self.as_expr(x), self.as_expr(y))

    def mod(self, x, y):
        if self.is_int(x) and self.is_int(y):
            return x % y
        return URem(self.as_expr(x), self.as_expr(y))

    def make_callable(self, node):
        t = node['type']
        if t == 'ArrowFunctionExpression':
            assert not node['params']
            body = node['body']
            return lambda: self.eval(body)
        elif t == 'Identifier':
            name = node['name']
            return lambda: self.apply(name, [])
        else:
            raise NotImplementedError(f"callable node {t}")

    def ite(self, cond, true_fn, false_fn):
        t_val = true_fn()
        f_val = false_fn()
        if isinstance(cond, bool):
            return t_val if cond else f_val
        if self.is_int(cond):
            return t_val if cond else f_val
        cond_expr = self.as_expr(cond)
        return If(cond_expr != ZERO, self.as_expr(t_val), self.as_expr(f_val))

    def get_char(self, idx):
        if isinstance(idx, int):
            pass
        elif hasattr(idx, 'as_long'):
            idx = idx.as_long()
        else:
            raise ValueError(f"non-constant index {idx}")
        if not (0 <= idx < self.length):
            raise IndexError(f"index {idx} out of range")
        return self.chars[idx]

    def apply(self, name, args):
        if name == 'a':
            return 0
        if name == 'b':
            return self.add(args[0], args[1])
        if name == 'c':
            return self.mul(args[0], args[1])
        if name == 'd':
            assert self.is_int(args[0]) and self.is_int(args[1])
            return args[0] ** args[1]
        if name == 'e':
            return self.band(args[0], args[1])
        if name == 'g':
            assert args[0] == '__input__'
            return self.get_char(args[1])
        if name == 'h':
            return self.length
        if name == 'A':
            return self.wrap(self.sub(args[0], args[1]), 8)
        if name == 'B':
            return self.wrap(self.sub(args[0], args[1]), 16)
        if name == 'C' or name == 'F':
            pred = self.ge(args[0], args[1])
            if isinstance(pred, bool):
                return 1 if pred else 0
            return If(pred, ONE, ZERO)
        if name == 'D':
            return self.wrap(self.sub(args[1], self.shr8(args[0])), 16)
        if name == 'E':
            return self.shr8(args[0])
        if name == 'G':
            return self.add(args[2], self.div(args[0], args[1]))
        if name == 'H':
            return self.div(args[0], args[1])
        if name == 'I':
            return self.mod(args[0], args[1])
        if name == 'J':
            raise RuntimeError('nested J not expected')
        if name == 'K':
            raise RuntimeError('K not used here')
        raise NotImplementedError(f"Unknown func {name}")

    def eval(self, node):
        t = node['type']
        if t == 'CallExpression':
            callee = node['callee']
            if callee['type'] != 'Identifier':
                raise NotImplementedError('non-identifier callee')
            name = callee['name']
            if name == 'f':
                cond = self.eval(node['arguments'][0])
                true_fn = self.make_callable(node['arguments'][1])
                false_fn = self.make_callable(node['arguments'][2])
                return self.ite(cond, true_fn, false_fn)
            else:
                args = [self.eval(arg) for arg in node['arguments']]
                return self.apply(name, args)
        elif t == 'Identifier':
            name = node['name']
            if name == 'x':
                return '__input__'
            return lambda: self.apply(name, [])
        elif t == 'ArrowFunctionExpression':
            assert not node['params']
            return lambda: self.eval(node['body'])
        elif t == 'Literal':
            return node['value']
        else:
            raise NotImplementedError(f"Unsupported node type {t}")

    def solve(self):
        expr = self.eval(self.ast['body'])
        self.solver.add(expr != ZERO)
        if self.solver.check() != sat:
            raise RuntimeError('No solution')
        model = self.solver.model()
        chars = [chr(model[ch].as_long()) for ch in self.chars]
        return ''.join(chars)

interp = Interpreter(J_AST)
solution = interp.solve()
print(solution)
