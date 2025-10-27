import socket

HOST = "snek.challs.m0lecon.it"
PORT = 28027
replay = b'.'

with socket.create_connection((HOST, PORT)) as s:
    def recv_until(pattern):
        data = b''
        while not data.endswith(pattern):
            chunk = s.recv(1)
            if not chunk:
                break
            data += chunk
        return data
    print(recv_until(b'Replay size: '))
    s.sendall(str(len(replay)).encode() + b"\n")
    print(recv_until(b'Replay data: '))
    s.sendall(replay)
    print(recv_until(b'Download game screenshot (y/n)? '))
    s.sendall(b"y\n")
    data = b''
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        data += chunk

print('Received', len(data), 'bytes')
open('remote.png', 'wb').write(data)
print('PNG saved to remote.png')
