from PIL import Image
import numpy as np

img = Image.open("remote.png").convert("L")
arr = np.array(img)
height, width = arr.shape
for tile_x in range(width // 20):
    block = arr[0:20, tile_x*20:(tile_x+1)*20]
    mean = block.mean()
    if mean < 250:  # some content
        print(tile_x, mean)
