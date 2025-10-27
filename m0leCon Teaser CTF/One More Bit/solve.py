import json
import socket
from typing import Iterable


HOST = "one-more-bit.challs.m0lecon.it"
PORT = 24180
BIT_POSITIONS: tuple[int, ...] = tuple(range(24))
THRESHOLD = 6


def query_bits(sock_file, state_index: int, positions: Iterable[int]) -> list[int]:
    bits: list[int] = []
    # Send all requests first to minimize round-trip overhead.
    for pos in positions:
        request = json.dumps({"command": "decrypt", "index": state_index, "position": pos})
        sock_file.write(request + "\n")
    sock_file.flush()

    for pos in positions:
        line = sock_file.readline()
        if not line:
            raise RuntimeError("connection closed while reading decrypt responses")
        response = json.loads(line)
        if response.get("status") != "ok":
            raise RuntimeError(f"decrypt failed at position {pos}: {response}")
        bits.append(int(response["bit"]))
    return bits


def solve() -> None:
    with socket.create_connection((HOST, PORT)) as sock:
        sock_file = sock.makefile("rw", buffering=1, encoding="utf-8", newline="\n")

        while True:
            line = sock_file.readline()
            if not line:
                print("Connection closed by server.")
                return
            data = json.loads(line)

            status = data.get("status")
            if status == "new_round":
                # Fresh round: set up challenge instance.
                encrypt_req = json.dumps({"command": "encrypt", "m0": 0.0, "m1": 1.0})
                sock_file.write(encrypt_req + "\n")
                sock_file.flush()
                encrypt_resp = json.loads(sock_file.readline())
                state_index = int(encrypt_resp["state_index"])

                bits = query_bits(sock_file, state_index, BIT_POSITIONS)
                score = sum(bits)
                guess_bit = 1 if score >= THRESHOLD else 0

                guess_req = json.dumps({"command": "guess", "bit": guess_bit})
                sock_file.write(guess_req + "\n")
                sock_file.flush()
                result_resp = json.loads(sock_file.readline())
                if result_resp.get("result") == "LOSE":
                    print("Wrong guess, aborting.")
                    return

            elif status == "ok" and "flag" in data:
                print(data["flag"])
                return
            else:
                # Unexpected message; just print and continue/abort as needed.
                print(f"Unexpected message: {data}")
                return


if __name__ == "__main__":
    solve()
