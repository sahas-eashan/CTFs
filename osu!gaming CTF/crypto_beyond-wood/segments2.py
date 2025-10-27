import numpy as np
from PIL import Image
img = Image.open("crop_ext0_erode.png")
arr = np.array(img)
col_sum = (arr < 128).sum(axis=0)
threshold = 3
segments = []
in_char = False
start = 0
for i, val in enumerate(col_sum):
    if val > threshold and not in_char:
        in_char = True
        start = i
    elif val <= threshold and in_char:
        if i - start > 3:
            segments.append((start, i))
        in_char = False
if in_char:
    segments.append((start, len(col_sum)))
print(len(segments), segments[:20])
