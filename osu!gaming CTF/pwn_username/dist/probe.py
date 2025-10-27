import socket
import time

HOST = "username-checker.challs.sekai.team"
PORT = 1337
TIMEOUT = 6

# Payloads exercise various lengths and format-specifiers to provoke bugs.
TESTS = [
    b"test\n",
    b"A\n",
    b"A" * 32 + b"\n",
    b"A" * 128 + b"\n",
    b"A" * 512 + b"\n",
    b"A" * 1024 + b"\n",
    b"%x\n",
    b"%p\n",
    b"%s\n",
    b"%%n\n",
    b"\n",
]


def recv_all(sock: socket.socket, timeout: float = 1.0) -> bytes:
    """Read whatever data is immediately available without blocking long."""
    sock.settimeout(timeout)
    chunks = []
    try:
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            chunks.append(chunk)
            if len(chunk) < 4096:
                break
    except Exception:
        pass
    return b"".join(chunks)


def run_probe() -> None:
    """Cycle through canned payloads and print banner/response pairs."""
    for payload in TESTS:
        print("=" * 60)
        display = payload[:60]
        if len(payload) > 60:
            display += b"..."
        print(f"Sending: {display!r}")

        try:
            with socket.create_connection((HOST, PORT), timeout=TIMEOUT) as sock:
                banner = recv_all(sock, timeout=1.0)
                print("BANNER:")
                print(banner.decode(errors="replace"))

                sock.sendall(payload)
                time.sleep(0.2)

                response = recv_all(sock, timeout=1.0)
                print("RESPONSE:")
                print(response.decode(errors="replace"))
        except Exception as exc:  # Connection dropped, timeout, etc.
            print(f"ERROR: {exc}")
        print()


if __name__ == "__main__":
    run_probe()
