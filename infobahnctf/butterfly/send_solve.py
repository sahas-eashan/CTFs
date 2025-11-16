
import socket
import time

# It's important to add a timeout to the socket
# because the server might not respond
# or the exploit might crash it
TIMEOUT = 5 # seconds

def solve():
    try:
        with open("solve.js", "r") as f:
            script = f.read()
    except FileNotFoundError:
        print("solve.js not found")
        return

    HOST = "the-butterfly-effect.challs.infobahnc.tf"
    PORT = 1337

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            try:
                s.connect((HOST, PORT))
            except (socket.timeout, ConnectionRefusedError) as e:
                print(f"Failed to connect to {HOST}:{PORT}: {e}")
                return

            # The server expects the size first
            s.sendall(f"{len(script)}\n".encode())

            # Then the script
            s.sendall(script.encode())

            # Wait for the server to respond
            time.sleep(1)

            # Try to receive data
            try:
                response = s.recv(4096).decode()
                print(response)
            except socket.timeout:
                print("Socket timed out waiting for response")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    solve()
