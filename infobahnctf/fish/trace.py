import io
import pathlib
import sys

import fish


def main() -> None:
    code = pathlib.Path("chall.txt").read_text()
    interpreter = fish.Interpreter(code)

    fake_input = io.StringIO("320\n")
    fake_input.isatty = lambda: False  # type: ignore[attr-defined]

    original_stdin, original_stdout = sys.stdin, sys.stdout
    capture = io.StringIO()

    try:
        sys.stdin = fake_input
        sys.stdout = capture

        step = 0
        history_limit = 200

        while True:
            instr = interpreter.move()

            if step < history_limit:
                stack_view = interpreter._stack[-5:]
                print(f"step={step:05d} instr={repr(instr)} stack={stack_view}")

            if (
                instr == "%"
                and len(interpreter._stack) >= 1
                and interpreter._stack[-1] == 0
            ):
                print(f"modulo hit zero at step {step}")
                break

            step += 1

        follow_up = 200
        for extra in range(follow_up):
            instr = interpreter.move()
            stack_view = interpreter._stack[-5:]
            print(f"post={extra:03d} instr={repr(instr)} stack={stack_view}")
    except fish.StopExecution:
        print("program halted")
    finally:
        sys.stdin = original_stdin
        sys.stdout = original_stdout

    print("captured output:", capture.getvalue())


if __name__ == "__main__":
    main()
