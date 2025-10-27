from PIL import Image
import numpy as np

img = Image.open("remote_gameover.png").convert("L")
arr = np.array(img)

BLOCK_W = 5
BLOCK_H = 10

def downsample(tx, ty, thr=200):
    tile = arr[ty*20:(ty+1)*20, tx*20:(tx+1)*20]
    h, w = tile.shape
    bh = h // BLOCK_H
    bw = w // BLOCK_W
    pattern = []
    for by in range(BLOCK_H):
        line = ''
        for bx in range(BLOCK_W):
            block = tile[by*bh:(by+1)*bh, bx*bw:(bx+1)*bw]
            line += '#' if block.mean() > thr else '.'
        pattern.append(line)
    return pattern

coords = [(0,0),(9,0)]
for coord in coords:
    pattern = downsample(*coord, thr=200)
    print(coord)
    for line in pattern:
        print(line)
    print()
