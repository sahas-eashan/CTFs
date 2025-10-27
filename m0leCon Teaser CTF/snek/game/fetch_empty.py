import socket
HOST="snek.challs.m0lecon.it"
PORT=28027
with socket.create_connection((HOST,PORT)) as s:
    def recv_until(pat):
        buf=b''
        while not buf.endswith(pat):
            chunk=s.recv(1)
            if not chunk:
                break
            buf+=chunk
        return buf
    recv_until(b"Replay size: ")
    s.sendall(b"0\n")
    recv_until(b"Replay data: ")
    s.sendall(b"")
    recv_until(b"Download game screenshot (y/n)? ")
    s.sendall(b"y\n")
    data=b''
    while True:
        chunk=s.recv(4096)
        if not chunk:
            break
        data+=chunk
with open("screen_empty.png","wb") as f:
    f.write(data)
