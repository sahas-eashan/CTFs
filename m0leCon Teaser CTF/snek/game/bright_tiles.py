from PIL import Image
import numpy as np

img = Image.open("remote_gameover.png").convert("L")
arr = np.array(img)
for ty in range(arr.shape[0]//20):
    for tx in range(arr.shape[1]//20):
        block = arr[ty*20:(ty+1)*20, tx*20:(tx+1)*20]
        if block.mean() > 20:  # pick up digits
            print((tx, ty), block.mean(), block.max())
