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

def segment_on(tile, seg):
    (y1,y2),(x1,x2) = segments[seg]
    block = tile[y1:y2, x1:x2]
    return block.mean() > 100

coords = [(0,0),(9,0)]
for tx, ty in coords:
    tile = arr[ty*20:(ty+1)*20, tx*20:(tx+1)*20]
    active = [seg for seg in segments if segment_on(tile, seg)]
    print((tx,ty), active)
