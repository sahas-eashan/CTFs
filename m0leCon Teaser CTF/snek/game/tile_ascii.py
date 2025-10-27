from PIL import Image
import numpy as np

img = Image.open("remote.png").convert("L")
arr = np.array(img)

def print_tile(tile_x, tile_y, thr=150):
    x0, y0 = tile_x*20, tile_y*20
    tile = arr[y0:y0+20, x0:x0+20]
    for row in tile:
        print(''.join('#' if v < thr else '.' for v in row))
    print()

print_tile(8,5)
