from PIL import Image
import numpy as np

img = Image.open("remote.png").convert("L")
arr = np.array(img)
for tile_x in range(10):
    block = arr[100:120, tile_x*20:(tile_x+1)*20]
    mean = block.mean()
    if mean < 240:
        print(tile_x, mean)
