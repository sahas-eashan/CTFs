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

DIGITS = {
    frozenset(['top','upper_right','lower_right','bottom','middle']): '3',
    frozenset(['top','upper_right','middle','lower_left','bottom']): '2',
    frozenset(['top','upper_left','upper_right','lower_left','lower_right','bottom']): '0',
    frozenset(['top','upper_left','upper_right','middle','lower_right','bottom']): '9',
    frozenset(['top','upper_left','upper_right','middle','lower_left','lower_right','bottom']): '8',
    frozenset(['top','upper_left','lower_left','lower_right','bottom','middle']): '6',
    frozenset(['upper_left','upper_right','middle','lower_right']): '4',
    frozenset(['top','upper_left','middle','lower_right','bottom']): '5',
    frozenset(['top','upper_right','lower_right']): '7',
    frozenset(['top','upper_right','lower_right','bottom']): '1',
}

coords = [(0,0),(9,0),(0,7),(9,7),(0,8),(9,8)]
for tx, ty in coords:
    tile = arr[ty*20:(ty+1)*20, tx*20:(tx+1)*20]
    active = []
    for seg,(yr,xr) in segments.items():
        (y1,y2),(x1,x2) = segments[seg]
        block = tile[y1:y2, x1:x2]
        if block.mean() > 120:
            active.append(seg)
    digit = DIGITS.get(frozenset(active), '?')
    print((tx,ty), active, digit)
