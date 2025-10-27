from PIL import Image
import numpy as np

img = Image.open("remote.png").convert("L")
# Crop area where digits appear
crop = img.crop((0, 90, 200, 140))
arr = np.array(crop)
scale = 1
chars = " .:-=+*#%@"
for y in range(0, arr.shape[0], scale):
    line = []
    for x in range(0, arr.shape[1], scale):
        val = arr[y, x]
        line.append(chars[int(val / 255 * (len(chars)-1))])
    print(''.join(line))
