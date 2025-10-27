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

DIGITS = {
    frozenset(['top','middle','bottom','upper_right','lower_right']): '3',
    frozenset(['top','middle','bottom','upper_right','lower_left']): '2',
    frozenset(['top','upper_right','lower_right']): '7',
    frozenset(['top','bottom','upper_right','lower_right']): '1',
    frozenset(['top','upper_left','upper_right','lower_left','lower_right','bottom']): '0',
    frozenset(['top','upper_left','upper_right','middle','lower_right']): '4',
    frozenset(['top','upper_left','middle','lower_right','bottom']): '5',
    frozenset(['top','upper_left','middle','lower_left','lower_right','bottom']): '6',
    frozenset(['top','upper_right','middle','lower_left','bottom']): '2',
    frozenset(['top','upper_left','upper_right','middle','lower_right','bottom']): '9',
    frozenset(['top','middle','bottom','upper_left','upper_right','lower_left','lower_right']): '8'
}

coords = [(0,0),(9,0)]

def decode_digits(path):
    arr = np.array(Image.open(path).convert('L'))
    digits = []
    for tx, ty in coords:
        tile = arr[ty*20:(ty+1)*20, tx*20:(tx+1)*20]
        active = []
        for seg in segments:
            (y1,y2),(x1,x2) = segments[seg]
            block = tile[y1:y2, x1:x2]
            if block.mean() > 80:
                active.append(seg)
        digit = DIGITS.get(frozenset(active), '?')
        digits.append(digit)
    return ''.join(digits)

def fetch(replay_path, output_path):
    data = Path(replay_path).read_bytes()
    with socket.create_connection((HOST, PORT)) as s:
        def recv_until(pattern):
            buf = b''
            while not buf.endswith(pattern):
                chunk = s.recv(1)
                if not chunk:
                    break
                buf += chunk
            return buf
        recv_until(b"Replay size: ")
        s.sendall(str(len(data)).encode() + b"\n")
        recv_until(b"Replay data: ")
        s.sendall(data)
        recv_until(b"Download game screenshot (y/n)? ")
        s.sendall(b"y\n")
        img = b''
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            img += chunk
    Path(output_path).write_bytes(img)
    return output_path

if __name__ == '__main__':
    prefixes = sorted(Path('.').glob('replay_prefix*.txt'))
    for idx, path in enumerate(prefixes,1):
        out = f"screen_prefix{idx}.png"
        fetch(path, out)
        digits = decode_digits(out)
        print(path.name, digits)
