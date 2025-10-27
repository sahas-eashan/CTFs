from PIL import Image
import numpy as np
img = Image.open("remote_gameover.png").convert("L")
arr = np.array(img)
for ty in range(10):
    for tx in range(10):
        block = arr[ty*20:(ty+1)*20, tx*20:(tx+1)*20]
        mean = block.mean()
        if 140 < mean < 200:
            print((tx, ty), mean)
