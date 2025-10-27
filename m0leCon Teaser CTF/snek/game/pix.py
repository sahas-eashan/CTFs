from PIL import Image
img = Image.open("remote_gameover.png").convert("L")
pixels = img.load()
for y in range(20):
    row = [pixels[x,y] for x in range(20)]
    print(row)
