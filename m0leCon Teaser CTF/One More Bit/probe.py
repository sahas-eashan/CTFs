import json
import socket


def main() -> None:
    host = "one-more-bit.challs.m0lecon.it"
    port = 24180

    with socket.create_connection((host, port)) as sock:
        sock_file = sock.makefile("rw", buffering=1, encoding="utf-8", newline="\n")

        while True:
            line = sock_file.readline()
            if not line:
                print("[server closed]")
                return
            line = line.strip()
            if not line:
                continue
            print(f"[server] {line}")

            data = json.loads(line)
            if data.get("status") != "new_round":
                break

            # Simple probing sequence per round
            requests = [
                {"command": "encrypt", "m0": 0.0, "m1": 1.0},
                {"command": "eval", "function": "square", "indices": [0]},
                {"command": "eval", "function": "square", "indices": [1]},
                {"command": "eval", "function": "square", "indices": [2]},
                {"command": "eval", "function": "square", "indices": [3]},
                {"command": "eval", "function": "square", "indices": [4]},
                {"command": "decrypt", "index": 5, "position": 0},
                {"command": "guess", "bit": 0},
            ]

            for req in requests:
                payload = json.dumps(req)
                print(f"[client] {payload}")
                sock_file.write(payload + "\n")
                sock_file.flush()
                resp = sock_file.readline()
                if not resp:
                    print("[server closed]")
                    return
                print(f"[server] {resp.strip()}")


if __name__ == "__main__":
    main()
