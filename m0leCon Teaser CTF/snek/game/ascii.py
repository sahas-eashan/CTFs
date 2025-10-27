from PIL import Image
import numpy as np

img = Image.open("remote.png").convert("L")
arr = np.array(img)
scale = 2
for y in range(0, arr.shape[0], scale):
    line = []
    for x in range(0, arr.shape[1], scale):
        block = arr[y:y+scale, x:x+scale]
        val = block.mean()
        line.append('#' if val < 200 else ' ')
    print(''.join(line))
    if y >= 120:
        break
