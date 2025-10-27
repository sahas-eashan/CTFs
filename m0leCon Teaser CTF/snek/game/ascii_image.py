from PIL import Image
import numpy as np

img = Image.open("remote_gameover.png").convert("L")
arr = np.array(img)
chars = {True:'#', False:' '}
scale = 4
for y in range(0, arr.shape[0], scale):
    row = ''.join('#' if arr[y, x] > 200 else ' ' for x in range(0, arr.shape[1], scale))
    print(row)
