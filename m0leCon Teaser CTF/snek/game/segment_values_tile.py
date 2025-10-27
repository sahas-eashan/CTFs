from PIL import Image
import numpy as np

img = Image.open("remote_gameover.png").convert("L")
arr = np.array(img)
segments = {
    'top': ((2,4),(4,16)),
    'middle': ((9,11),(4,16)),
    'bottom': ((16,18),(4,16)),
    'upper_left': ((4,9),(4,6)),
    'upper_right': ((4,9),(14,16)),
    'lower_left': ((11,16),(4,6)),
    'lower_right': ((11,16),(14,16)),
}
coords = [(0,7),(9,7),(0,8),(9,8)]
for tx, ty in coords:
    tile = arr[ty*20:(ty+1)*20, tx*20:(tx+1)*20]
    print('tile', (tx,ty))
    for seg in segments:
        (y1,y2),(x1,x2) = segments[seg]
        block = tile[y1:y2, x1:x2]
        print(seg, block.mean())
    print()
