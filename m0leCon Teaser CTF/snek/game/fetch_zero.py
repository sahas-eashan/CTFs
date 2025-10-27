import socket
HOST="snek.challs.m0lecon.it"
PORT=28027
data=b'.'
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
    s.sendall(b"1\n")
    recv_until(b"Replay data: ")
    s.sendall(data)
    recv_until(b"Download game screenshot (y/n)? ")
    s.sendall(b"y\n")
    img=b''
    while True:
        chunk=s.recv(4096)
        if not chunk:
            break
        img+=chunk
with open("screen_zero.png","wb") as f:
    f.write(img)
