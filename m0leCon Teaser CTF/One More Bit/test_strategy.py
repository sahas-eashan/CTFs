import json
import socket


def run_trial() -> bool:
    host = "one-more-bit.challs.m0lecon.it"
    port = 24180

    with socket.create_connection((host, port)) as sock:
        sock_file = sock.makefile("rw", buffering=1, encoding="utf-8", newline="\n")

        line = sock_file.readline()
        if not line:
            return False
        data = json.loads(line)
        assert data["status"] == "new_round"

        # Query encrypt oracle with plain pair (0, 1)
        req = json.dumps({"command": "encrypt", "m0": 0.0, "m1": 2.0 ** -51})
        sock_file.write(req + "\n")
        sock_file.flush()
        _ = json.loads(sock_file.readline())

        # Ask for LSB and use it as biased coin for the challenge bit
        sock_file.write(json.dumps({"command": "decrypt", "index": 0, "position": 0}) + "\n")
        sock_file.flush()
        decrypt_resp = json.loads(sock_file.readline())
        bit = decrypt_resp["bit"]

        guess = bit & 1
        sock_file.write(json.dumps({"command": "guess", "bit": guess}) + "\n")
        sock_file.flush()
        guess_resp = json.loads(sock_file.readline())

        return guess_resp.get("result") == "WIN"


def main() -> None:
    wins = 0
    tries = 20

    for _ in range(tries):
        if run_trial():
            wins += 1

    print(f"Wins: {wins}/{tries}")


if __name__ == "__main__":
    main()
