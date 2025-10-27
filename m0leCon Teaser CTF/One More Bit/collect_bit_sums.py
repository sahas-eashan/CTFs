import json
import socket


def run_trial(bits: list[int]) -> tuple[int, list[int]]:
    host = "one-more-bit.challs.m0lecon.it"
    port = 24180

    with socket.create_connection((host, port)) as sock:
        sock_file = sock.makefile("rw", buffering=1, encoding="utf-8", newline="\n")

        line = sock_file.readline()
        if not line:
            raise RuntimeError("no greeting from server")
        data = json.loads(line)
        assert data["status"] == "new_round"

        sock_file.write(json.dumps({"command": "encrypt", "m0": 0.0, "m1": 1.0}) + "\n")
        sock_file.flush()
        sock_file.readline()

        results: list[int] = []

        for bit_index in bits:
            sock_file.write(json.dumps({"command": "decrypt", "index": 0, "position": bit_index}) + "\n")
            sock_file.flush()
            resp = json.loads(sock_file.readline())
            if resp.get("status") == "ok":
                results.append(resp["bit"])
            else:
                results.append(-1)

        sock_file.write(json.dumps({"command": "guess", "bit": 0}) + "\n")
        sock_file.flush()
        guess_resp = json.loads(sock_file.readline())
        actual_bit = 0 if guess_resp.get("result") == "WIN" else 1

        return actual_bit, results


def main() -> None:
    bits = list(range(0, 24))
    trials = 30
    sums = {0: [], 1: []}

    for _ in range(trials):
        actual, values = run_trial(bits)
        filtered = [v for v in values if v >= 0]
        sums[actual].append(sum(filtered))

    for actual in [0, 1]:
        scores = sums[actual]
        count = len(scores)
        avg = sum(scores) / count if count else 0.0
        print(f"challenge_bit={actual}: count={count}, avg_ones={avg:.2f}, min={min(scores, default=0)}, max={max(scores, default=0)}")
        print(f"  values={scores}")


if __name__ == "__main__":
    main()
