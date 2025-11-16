import io
import pathlib
import sys
from collections import defaultdict

import fish


def main() -> None:
    code = pathlib.Path("chall.txt").read_text()

    writes: list[tuple[int, int, int]] = []  # (x, y, value)
    outputs: list[int] = []

    original_handle = fish.Interpreter._handle_instruction

    def hooked(self: fish.Interpreter, instruction: str) -> None:
        if instruction == "p" and len(self._stack) >= 3:
            x = int(self._stack[-1])
            y = int(self._stack[-2])
            z = int(self._stack[-3])
            writes.append((x, y, z))
        elif instruction == "o" and self._stack:
            outputs.append(int(self._stack[-1]))
        return original_handle(self, instruction)

    fish.Interpreter._handle_instruction = hooked  # type: ignore[assignment]

    try:
        interpreter = fish.Interpreter(code)

        fake_input = io.StringIO("320\n")
        fake_input.isatty = lambda: False  # type: ignore[attr-defined]

        original_stdin = sys.stdin
        sys.stdin = fake_input

        max_steps = 20_000_000
        max_writes = 500

        for step in range(max_steps):
            if len(writes) >= max_writes:
                print(f"[info] stopping early after capturing {len(writes)} writes")
                break

            try:
                interpreter.move()
            except fish.StopExecution:
                break
        else:
            print(f"[warn] reached {max_steps} steps without halting")

    finally:
        fish.Interpreter._handle_instruction = original_handle  # type: ignore[assignment]
        sys.stdin = original_stdin

    print(f"writes captured: {len(writes)}")
    if outputs:
        decoded = "".join(chr(o) for o in outputs)
        print(f"direct output: {decoded!r}")
    else:
        print("no direct output captured")

    if writes:
        ordered = "".join(
            chr(z) if 32 <= z < 127 else f"\\x{z:02x}" for _, _, z in writes
        )
        print(f"write values (ordered): {ordered}")

    grid: dict[int, dict[int, int]] = defaultdict(dict)
    for x, y, z in writes:
        grid[y][x] = z

    rows = sorted(grid.keys())
    print(f"grid rows: {rows[:10]} ...")

    for y in rows:
        row = grid[y]
        min_x = min(row.keys())
        max_x = max(row.keys())
        line_chars = []
        for x in range(min_x, max_x + 1):
            val = row.get(x, 32)
            if 32 <= val < 127:
                line_chars.append(chr(val))
            else:
                line_chars.append(f"\\x{val:02x}")
        print(f"y={y:03d} x[{min_x:03d}-{max_x:03d}]: {''.join(line_chars)}")


if __name__ == "__main__":
    main()
