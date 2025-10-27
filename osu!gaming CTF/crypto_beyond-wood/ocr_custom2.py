import numpy as np
from PIL import Image, ImageFont, ImageDraw

img = Image.open("crop_ext0_erode.png")
arr = np.array(img)
bin_img = (arr < 128).astype(np.uint8)
col_sum = bin_img.sum(axis=0)
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

font = ImageFont.load_default()
chars = []
for seg in segments:
    x1, x2 = seg
    char_bin = bin_img[:, x1:x2]
    rows = np.where(char_bin.sum(axis=1) > 0)[0]
    if len(rows) == 0:
        continue
    y1, y2 = rows[0], rows[-1]+1
    char_bin = char_bin[y1:y2, :]
    char_img = Image.fromarray((1-char_bin)*255)
    char_img = char_img.resize((20,30), Image.NEAREST)
    char_arr = np.array(char_img)/255.0
    best_char='?'
    best_score=-1
    for ch in "abcdefghijklmnopqrstuvwxyz0123456789_-{}":
        sample = Image.new('L',(20,30),255)
        draw = ImageDraw.Draw(sample)
        bbox = font.getbbox(ch)
        w = bbox[2]-bbox[0]
        h = bbox[3]-bbox[1]
        draw.text(((20-w)/2, (30-h)/2), ch, font=font, fill=0)
        sample_arr = np.array(sample)/255.0
        num = np.sum((1-char_arr)*(1-sample_arr))
        denom = np.sqrt(np.sum((1-char_arr)**2)*np.sum((1-sample_arr)**2))
        score = num/denom if denom else 0
        if score > best_score:
            best_score=score
            best_char=ch
    chars.append(best_char)
print('segments',segments)
print('decoded',''.join(chars))
