import io
import pathlib
import sys
import time

import fish


def main() -> None:
    code = pathlib.Path("chall.txt").read_text()
    interpreter = fish.Interpreter(code)

    fake_input = io.StringIO("320\n")
    fake_input.isatty = lambda: False  # type: ignore[attr-defined]

    original_stdin, original_stdout = sys.stdin, sys.stdout
    buffer = io.StringIO()
    step_count = 0
    start_time = time.time()
    last_output_len = 0

    max_seconds = 120.0
    max_steps = 10_000_000
    debug_interval = 100_000

    try:
        sys.stdin = fake_input
        sys.stdout = buffer
        while True:
            interpreter.move()
            step_count += 1

            if step_count % debug_interval == 0 and step_count > 0:
                elapsed = time.time() - start_time
                original_stdout.write(
                    f"[debug] steps={step_count} elapsed={elapsed:.2f}s\n"
                )
                original_stdout.flush()

            current_value = buffer.getvalue()
            if len(current_value) > last_output_len:
                original_stdout.write(current_value[last_output_len:])
                original_stdout.flush()
                last_output_len = len(current_value)

            if time.time() - start_time > max_seconds:
                raise TimeoutError(
                    f"Interpreter execution exceeded {max_seconds:.0f} seconds"
                )

            if step_count >= max_steps:
                raise RuntimeError(
                    f"Interpreter exceeded {max_steps:,} steps without halting"
                )
    except fish.StopExecution:
        pass
    except TimeoutError as exc:
        original_stdout.write(f"[error] {exc}\n")
        original_stdout.flush()
    except RuntimeError as exc:
        original_stdout.write(f"[error] {exc}\n")
        original_stdout.flush()
    finally:
        sys.stdin = original_stdin
        sys.stdout = original_stdout

    print(buffer.getvalue())


if __name__ == "__main__":
    main()
