from PIL import Image
import numpy as np

img = Image.open("score_scaled.png").convert("L")
arr = np.array(img)
chars = " .:-=+*#%@"
for i, row in enumerate(arr):
    if i >= 40:
        break
    print(''.join(chars[int(v/255*(len(chars)-1))] for v in row))
