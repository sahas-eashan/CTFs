from PIL import Image
import numpy as np

img = Image.open("remote_gameover.png").convert("L")
arr = np.array(img)

def print_tile(tx, ty, thr):
    tile = arr[ty*20:(ty+1)*20, tx*20:(tx+1)*20]
    for row in tile:
        line = ''.join('#' if v>thr else '.' for v in row)
        print(line)
    print()

print_tile(0,7,120)
print_tile(9,7,120)
print_tile(0,8,120)
print_tile(9,8,120)
