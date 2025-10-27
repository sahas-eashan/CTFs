from PIL import Image
import numpy as np
segments = {
    'top': ((2,4),(4,16)),
    'middle': ((9,11),(4,16)),
    'bottom': ((16,18),(4,16)),
    'upper_left': ((4,9),(4,6)),
    'upper_right': ((4,9),(14,16)),
    'lower_left': ((11,16),(4,6)),
    'lower_right': ((11,16),(14,16)),
}
arr = np.array(Image.open('screen_zero.png').convert('L'))
for coords in [(0,0),(9,0)]:
    tx,ty = coords
    tile = arr[ty*20:(ty+1)*20, tx*20:(tx+1)*20]
    segs = {seg for seg,((y1,y2),(x1,x2)) in segments.items() if tile[y1:y2,x1:x2].mean()>50}
    print(coords, segs)
