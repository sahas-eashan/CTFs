import socket
from pathlib import Path
from PIL import Image
import numpy as np

HOST = "snek.challs.m0lecon.it"
PORT = 28027
segments = {
    'top': ((2,4),(4,16)),
    'middle': ((9,11),(4,16)),
    'bottom': ((16,18),(4,16)),
    'upper_left': ((4,9),(4,6)),
    'upper_right': ((4,9),(14,16)),
    'lower_left': ((11,16),(4,6)),
    'lower_right': ((11,16),(14,16)),
}
DIGIT_MAP = {
    frozenset(['top','middle','bottom','upper_right','lower_right']): '3',
    frozenset(['top','middle','bottom','upper_right','lower_left']): '2',
    frozenset(['top','middle','bottom','upper_left','upper_right','lower_left','lower_right']): '8',
    frozenset(['top','middle','bottom']): '-',
}
COORDS = [(0,0),(9,0)]

def decode(path):
    arr = np.array(Image.open(path).convert('L'))
    digits = []
    for tx,ty in COORDS:
        tile = arr[ty*20:(ty+1)*20, tx*20:(tx+1)*20]
        segs = {seg for seg,((y1,y2),(x1,x2)) in segments.items() if tile[y1:y2,x1:x2].mean()>50}
        digits.append(DIGIT_MAP.get(frozenset(segs), '?'))
    return ''.join(digits)

def fetch(replay_path, output_path):
    data = Path(replay_path).read_bytes()
    with socket.create_connection((HOST, PORT)) as s:
        def recv_until(pat):
            buf=b''
            while not buf.endswith(pat):
                chunk=s.recv(1)
                if not chunk:
                    break
                buf+=chunk
            return buf
        recv_until(b"Replay size: ")
        s.sendall(str(len(data)).encode()+b"\n")
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
    Path(output_path).write_bytes(img)

prefixes=sorted(Path('.').glob('apple_prefix*.txt'), key=lambda p:int(p.stem.replace('apple_prefix','')))
for p in prefixes:
    out=f"screen_{p.stem}.png"
    fetch(p, out)
    digits=decode(out)
    print(p.stem, digits)
