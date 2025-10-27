import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageOps

# Load and preprocess image
img = Image.open("crop_ext0.png").convert("L")
img = ImageOps.autocontrast(img)
arr = np.array(img)
# Normalize: convert to binary (text=1)
bin_img = (arr < 180).astype(np.uint8)
# Vertical projection to find character boundaries
col_sum = bin_img.sum(axis=0)
threshold = 5
segments = []
in_char = False
start = 0
for i, val in enumerate(col_sum):
    if val > threshold and not in_char:
        in_char = True
        start = i
    elif val <= threshold and in_char:
        if i - start > 5:  # ignore narrow noise
            segments.append((start, i))
        in_char = False
if in_char:
    segments.append((start, len(col_sum)))
print('segment count', len(segments))
# Merge segments that are very close
merged = []
for seg in segments:
    if merged and seg[0] - merged[-1][1] < 3:
        merged[-1] = (merged[-1][0], seg[1])
    else:
        merged.append(seg)
segments = merged
print('merged count', len(segments))
print('segments', segments)

# Candidate characters to compare
dictionary = list("abcdefghijklmnopqrstuvwxyz0123456789_-{}")
font = ImageFont.load_default()
results = []
for seg in segments:
    x1, x2 = seg
    char_img = bin_img[:, x1:x2]
    # remove leading/trailing blank rows
    row_sum = char_img.sum(axis=1)
    y_indices = np.where(row_sum > 0)[0]
    if len(y_indices) == 0:
        continue
    y1, y2 = y_indices[0], y_indices[-1] + 1
    char_img = char_img[y1:y2, :]
    char_img = Image.fromarray((1 - char_img) * 255)
    char_img = char_img.resize((20, 30), Image.NEAREST)
    char_arr = np.array(char_img) / 255.0
    best_char = None
    best_score = -1
    for ch in dictionary:
        sample = Image.new('L', (20, 30), 255)
        draw = ImageDraw.Draw(sample)
        w, h = draw.textsize(ch, font=font)
        draw.text(((20 - w)/2, (30 - h)/2), ch, font=font, fill=0)
        sample_arr = np.array(sample)/255.0
        # Compute correlation
        num = np.sum((1 - char_arr)*(1 - sample_arr))
        denom = np.sqrt(np.sum((1 - char_arr)**2) * np.sum((1 - sample_arr)**2))
        score = num / denom if denom else 0
        if score > best_score:
            best_score = score
            best_char = ch
    results.append((seg, best_char, best_score))
print(results)
print('decoded:', ''.join(ch for _, ch, _ in results))
