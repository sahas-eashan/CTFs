import numpy as np
from PIL import Image
img = Image.open("recovered.png").crop((70,65,456,245)).convert("L")
arr = np.array(img)
threshold = 122
bin = (arr <= threshold).astype(int)
block = 12
h, w = bin.shape
h_blocks = h // block
w_blocks = w // block
for y in range(h_blocks):
    row = ""
    for x in range(w_blocks):
        sub = bin[y*block:(y+1)*block, x*block:(x+1)*block]
        row += "#" if sub.mean() > 0.5 else " "
    if "#" in row:
        print(row)
