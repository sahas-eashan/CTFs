from PIL import Image
import numpy as np
img = Image.open('screen_prefix1.png').convert('L')
tile = np.array(img)[0:20,0:20]
for row in tile:
    print(''.join(f"{v:03d}" for v in row))
