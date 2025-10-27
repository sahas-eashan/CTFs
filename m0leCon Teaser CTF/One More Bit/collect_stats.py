import collections
import json
import socket
from typing import Counter, Dict, Tuple


def run_trial(m0: float, m1: float, bit_index: int) -> Tuple[int, int] | None:
    host = "one-more-bit.challs.m0lecon.it"
    port = 24180

    with socket.create_connection((host, port)) as sock:
        sock_file = sock.makefile("rw", buffering=1, encoding="utf-8", newline="\n")

        line = sock_file.readline()
        if not line:
            raise RuntimeError("no greeting from server")
        data = json.loads(line)
        assert data["status"] == "new_round"

        sock_file.write(json.dumps({"command": "encrypt", "m0": m0, "m1": m1}) + "\n")
        sock_file.flush()
        sock_file.readline()

        sock_file.write(json.dumps({"command": "decrypt", "index": 0, "position": bit_index}) + "\n")
        sock_file.flush()
        decrypt_resp = json.loads(sock_file.readline())
        if decrypt_resp.get("status") != "ok":
            return None
        bit = decrypt_resp["bit"]

        sock_file.write(json.dumps({"command": "guess", "bit": 0}) + "\n")
        sock_file.flush()
        guess_resp = json.loads(sock_file.readline())

        actual_bit = 0 if guess_resp.get("result") == "WIN" else 1
        return actual_bit, bit


def collect(m0: float, m1: float, bit_index: int, trials: int = 20) -> Counter[Tuple[int, int]]:
    stats: Counter[Tuple[int, int]] = collections.Counter()
    for _ in range(trials):
        result = run_trial(m0, m1, bit_index)
        if result is not None:
            stats[result] += 1
    return stats


def main() -> None:
    m0 = 0.0
    m1 = 1.0
    max_bit = 10
    trials = 10

    print(f"Collecting stats for m0={m0}, m1={m1}, trials={trials}")
    for bit_index in range(max_bit + 1):
        stats = collect(m0, m1, bit_index, trials=trials)
        total = sum(stats.values())
        if total == 0:
            print(f"bit {bit_index}: denied")
            continue
        print(f"bit {bit_index}: total={total}")
        for actual in [0, 1]:
            for observed in [0, 1]:
                count = stats[(actual, observed)]
                print(f"  actual={actual} observed={observed} count={count}")


if __name__ == "__main__":
    main()
