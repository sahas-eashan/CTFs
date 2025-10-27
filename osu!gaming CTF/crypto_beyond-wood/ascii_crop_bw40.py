from PIL import Image
img = Image.open("recovered.png").crop((70,65,456,245)).convert("1")
img = img.resize((40, int(img.height*40/img.width/2)))
for y in range(img.height):
    row = ''.join('#' if pix==0 else ' ' for pix in img.crop((0,y,40,y+1)).getdata())
    if '#' in row:
        print(row)
