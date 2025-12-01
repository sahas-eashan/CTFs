import re
from pathlib import Path

def parse_instructions(path: str):
    text = Path(path).read_text(encoding='utf-16-le')
    instr_map = {}
    order = []
    for line in text.splitlines():
        m = re.match(r'\s*(\d+):\s+([^\s]+)(.*)', line)
        if not m:
            continue
        offset = int(m.group(1))
        opcode = m.group(2)
        rest = m.group(3)
        if '//' in rest:
            before, comment = rest.split('//', 1)
            comment = comment.strip()
        else:
            before, comment = rest, ''
        operand = before.strip()
        instr_map[offset] = {'op': opcode, 'operand': operand, 'comment': comment, 'raw': line}
        order.append(offset)
    order.sort()
    next_map = {order[i]: order[i+1] if i+1 < len(order) else None for i in range(len(order))}
    return instr_map, order[0], next_map

def wrap32(x):
    x &= 0xffffffff
    if x & 0x80000000:
        x -= 0x100000000
    return x

def wrap64(x):
    x &= 0xffffffffffffffff
    if x & 0x8000000000000000:
        x -= 0x10000000000000000
    return x

class VM:
    def __init__(self, instr_map, entry_pc, next_map):
        self.instr_map = instr_map
        self.next_map = next_map
        self.stack = []
        self.locals = [None]*50
        self.pc = entry_pc
        self.output = ''

    def push(self, value, typ):
        self.stack.append({'type': typ, 'value': value})

    def pop(self):
        if not self.stack:
            raise RuntimeError(f'empty stack at pc {self.pc}')
        return self.stack.pop()

    def pop_int(self):
        v = self.pop()
        if v['type'] not in ('int', 'char'):
            raise RuntimeError(f'int expected got {v} at pc {self.pc}')
        return v['value']

    def pop_long(self):
        v = self.pop()
        if v['type'] != 'long':
            raise RuntimeError(f'long expected got {v} at pc {self.pc}')
        return v['value']

    def load(self, idx):
        v = self.locals[idx]
        if v is None:
            raise RuntimeError(f'uninitialized local {idx} at pc {self.pc}')
        return {'type': v['type'], 'value': v['value']}

    def store(self, idx, value):
        self.locals[idx] = {'type': value['type'], 'value': value['value']}

    def handle_ldc(self, comment):
        if 'int' in comment:
            val = int(re.search(r'int\s+(-?\d+)', comment).group(1))
            self.push(val, 'int')
        elif 'String' in comment:
            s = comment.split('String', 1)[1].strip()
            self.push(s, 'string')
        else:
            raise RuntimeError(f'Unhandled ldc comment {comment}')

    def handle_ldc2(self, comment):
        if 'long' not in comment:
            raise RuntimeError(f'Unexpected ldc2 comment {comment}')
        val = int(re.search(r'long\s+(-?\d+)', comment).group(1))
        self.push(val, 'long')

    def dup(self):
        if not self.stack:
            raise RuntimeError('dup on empty stack')
        val = self.stack[-1]
        self.push(val['value'], val['type'])

    def dup2(self):
        if not self.stack:
            raise RuntimeError('dup2 on empty stack')
        top = self.stack[-1]
        if top['type'] == 'long':
            self.push(top['value'], top['type'])
        else:
            if len(self.stack) < 2:
                raise RuntimeError('dup2 needs two values')
            second = self.stack[-2]
            if second['type'] == 'long':
                raise RuntimeError('dup2 invalid combination')
            self.stack.extend([
                {'type': second['type'], 'value': second['value']},
                {'type': top['type'], 'value': top['value']}
            ])

    def run(self, max_steps=None, stop_at=None):
        steps = 0
        while self.pc is not None:
            if stop_at is not None and self.pc == stop_at:
                break
            if max_steps is not None and steps > max_steps:
                raise RuntimeError('too many steps')
            steps += 1
            # Fast-path the slow polynomial block
            if self.pc == 1712:
                self._handle_poly_block()
                self.pc = 1765
                continue

            inst = self.instr_map[self.pc]
            op = inst['op']
            operand = inst['operand']
            comment = inst['comment']
            nxt = self.next_map[self.pc]

            if op == 'getstatic':
                self.push('java/lang/System.out', 'ref')
            elif op in ('ldc', 'ldc_w'):
                self.handle_ldc(comment)
            elif op == 'ldc2_w':
                self.handle_ldc2(comment)
            elif op.startswith('istore_'):
                idx = int(op.split('_')[1])
                self.store(idx, self.pop())
            elif op == 'istore':
                idx = int(operand)
                self.store(idx, self.pop())
            elif op.startswith('iload_'):
                idx = int(op.split('_')[1])
                val = self.load(idx)
                self.push(val['value'], val['type'])
            elif op == 'iload':
                idx = int(operand)
                val = self.load(idx)
                self.push(val['value'], val['type'])
            elif op.startswith('lstore_'):
                idx = int(op.split('_')[1])
                val = self.pop()
                if val['type'] != 'long':
                    raise RuntimeError('lstore needs long')
                self.store(idx, val)
            elif op == 'lstore':
                idx = int(operand)
                val = self.pop()
                if val['type'] != 'long':
                    raise RuntimeError('lstore needs long')
                self.store(idx, val)
            elif op.startswith('lload_'):
                idx = int(op.split('_')[1])
                val = self.load(idx)
                if val['type'] != 'long':
                    raise RuntimeError('lload expects long')
                self.push(val['value'], val['type'])
            elif op == 'lload':
                idx = int(operand)
                val = self.load(idx)
                if val['type'] != 'long':
                    raise RuntimeError('lload expects long')
                self.push(val['value'], val['type'])
            elif op == 'iconst_0':
                self.push(0, 'int')
            elif op == 'iconst_1':
                self.push(1, 'int')
            elif op == 'iconst_m1':
                self.push(-1, 'int')
            elif op == 'lconst_0':
                self.push(0, 'long')
            elif op == 'lconst_1':
                self.push(1, 'long')
            elif op == 'iadd':
                b = self.pop_int(); a = self.pop_int()
                self.push(wrap32(a + b), 'int')
            elif op == 'isub':
                b = self.pop_int(); a = self.pop_int()
                self.push(wrap32(a - b), 'int')
            elif op == 'i2l':
                a = self.pop_int()
                self.push(a, 'long')
            elif op == 'i2c':
                a = self.pop_int()
                self.push(a & 0xffff, 'int')
            elif op == 'ladd':
                b = self.pop_long(); a = self.pop_long()
                self.push(wrap64(a + b), 'long')
            elif op == 'lsub':
                b = self.pop_long(); a = self.pop_long()
                self.push(wrap64(a - b), 'long')
            elif op == 'lcmp':
                b = self.pop_long(); a = self.pop_long()
                self.push(1 if a > b else -1 if a < b else 0, 'int')
            elif op == 'dup':
                self.dup()
            elif op == 'dup2':
                self.dup2()
            elif op == 'swap':
                self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]
            elif op == 'ifgt':
                target = int(operand)
                val = self.pop_int()
                self.pc = target if val > 0 else nxt
                continue
            elif op == 'ifne':
                target = int(operand)
                val = self.pop_int()
                self.pc = target if val != 0 else nxt
                continue
            elif op == 'ifeq':
                target = int(operand)
                val = self.pop_int()
                self.pc = target if val == 0 else nxt
                continue
            elif op == 'if_icmplt':
                target = int(operand)
                v2 = self.pop_int(); v1 = self.pop_int()
                self.pc = target if v1 < v2 else nxt
                continue
            elif op == 'if_icmpne':
                target = int(operand)
                v2 = self.pop_int(); v1 = self.pop_int()
                self.pc = target if v1 != v2 else nxt
                continue
            elif op == 'if_icmpge':
                target = int(operand)
                v2 = self.pop_int(); v1 = self.pop_int()
                self.pc = target if v1 >= v2 else nxt
                continue
            elif op == 'goto':
                self.pc = int(operand)
                continue
            elif op == 'invokevirtual':
                desc = comment
                if '(Ljava/lang/String;)V' in desc:
                    self.pop(); self.pop()
                elif '(C)V' in desc:
                    char_val = self.pop_int(); self.pop()  # pop object
                    self.output += chr(char_val & 0xffff)
                else:
                    raise RuntimeError(f'Unhandled invokevirtual {desc}')
            elif op == 'return':
                break
            else:
                raise RuntimeError(f'Unhandled op {op} at pc {self.pc}')

            self.pc = nxt
        return self.output

    def _handle_poly_block(self):
        # Simulates instructions 1712..1762 using direct multiplication
        # local3 determines the degree (1 or 2), local0 is the candidate value x
        local3 = self.locals[3]['value'] if self.locals[3] is not None else 0
        if local3 <= 0:
            return
        x_val = self.locals[0]['value']
        # Push n copies of x as long values (simulating instructions 1715..1725)
        for _ in range(local3):
            self.push(x_val, 'long')
        # Reset local6 to 0 as in the bytecode
        self.locals[6] = {'type': 'int', 'value': 0}
        # Perform the pairwise multiplications local3 times
        for i in range(local3):
            a = self.pop_long()
            b = self.pop_long()
            prod = wrap64(a * b)
            self.push(prod, 'long')
            # mirror updates to locals 6/8/10 for completeness
            self.locals[10] = {'type': 'long', 'value': a}
            self.locals[8] = {'type': 'long', 'value': b}
            self.locals[6] = {'type': 'int', 'value': i + 1}

def main():
    instr_map, entry_pc, next_map = parse_instructions('disasm.txt')
    vm = VM(instr_map, entry_pc, next_map)
    flag = vm.run()
    print(flag)

if __name__ == '__main__':
    main()
