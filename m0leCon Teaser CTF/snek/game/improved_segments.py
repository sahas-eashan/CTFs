from PIL import Image
import numpy as np
segments = {
    'top': ((2,5),(4,16)),
    'middle': ((9,11),(4,16)),
    'bottom': ((15,18),(4,16)),
    'upper_left': ((4,9),(3,7)),
    'upper_right': ((4,9),(13,17)),
    'lower_left': ((10,15),(3,7)),
    'lower_right': ((10,15),(13,17)),
}
arr = np.array(Image.open('screen_prefix1.png').convert('L'))
for coords in [(0,0),(9,0)]:
    tx,ty = coords
    tile = arr[ty*20:(ty+1)*20, tx*20:(tx+1)*20]
    segs = {seg for seg,((y1,y2),(x1,x2)) in segments.items() if tile[y1:y2,x1:x2].mean()>100}
    print(coords, segs)
