from PIL import Image
img = Image.open("remote.png")
pixels = img.load()
for y in range(0, 120):
    if y < 20 or y % 5 == 0:
        row = [pixels[x, y] for x in range(0, 200, 4)]
        unique = {px for px in row}
        print(y, len(unique))
