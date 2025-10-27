from PIL import Image
import numpy as np

img = Image.open("remote.png").convert("L")
arr = np.array(img)
scale = 2
chars = " .:-=+*#%@"
for y in range(90, 140, scale):
    line = []
    for x in range(0, arr.shape[1], scale):
        block = arr[y:y+scale, x:x+scale]
        val = int(block.mean() / 255 * (len(chars)-1))
        line.append(chars[val])
    print(''.join(line))
