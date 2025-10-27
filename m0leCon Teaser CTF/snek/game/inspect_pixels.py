from PIL import Image
img = Image.open("score.png").convert("L")
for y in range(0, 40):
    row = img.crop((0, y, img.width, y+1))
    values = list(row.getdata())
    if any(v < 250 for v in values):
        print(y, min(values), max(values))
