from PIL import Image
img = Image.open("recovered.png").crop((70,65,456,245)).convert("L")
img = img.point(lambda p: 255 if p>200 else 0)
img = img.resize((80, int(img.height*80/img.width/2)))
for y in range(img.height):
    row = ''.join('#' if p==0 else ' ' for p in img.crop((0,y,80,y+1)).getdata())
    if '#' in row:
        print(row)
