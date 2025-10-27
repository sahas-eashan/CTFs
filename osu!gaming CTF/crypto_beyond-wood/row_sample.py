from PIL import Image
img=Image.open("crop_ext0_bw.png")
width, height = img.size
row = height // 2
vals = [img.getpixel((x, row)) for x in range(width)]
block = 10
chars = []
for i in range(0, width, block):
    block_vals = vals[i:i + block]
    ratio = block_vals.count(0) / len(block_vals)
    chars.append('#' if ratio > 0.4 else ' ')
print(''.join(chars))
