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

for seg,(yr,xr) in segments.items():
    (y1,y2),(x1,x2) = segments[seg]
    block = arr[y1:y2, x1:x2]
    print('Tile0', seg, block.mean())

print('---')
tile = arr[0*20:(0+1)*20,9*20:(9+1)*20]
for seg,(yr,xr) in segments.items():
    (y1,y2),(x1,x2) = segments[seg]
    block = tile[y1:y2, x1:x2]
    print('Tile9', seg, block.mean())
