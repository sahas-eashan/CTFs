from PIL import Image
import numpy as np

img = Image.open("remote.png").convert("L")
arr = np.array(img)
chars = " .:-=+*#%@"
for y in range(0, 32):
    line = ''.join(chars[int(arr[y,x]/255*(len(chars)-1))] for x in range(arr.shape[1]))
    print(line)
