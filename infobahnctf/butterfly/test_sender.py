import socket
import time

with open("test_simple.js", "r") as f:
    script = f.read()

HOST = "the-butterfly-effect.challs.infobahnc.tf"
PORT = 1337

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(10)
    s.connect((HOST, PORT))
    s.sendall(f"{len(script)}\n".encode())
    s.sendall(script.encode())
    time.sleep(2)
    response = s.recv(4096).decode()
    print(response)
