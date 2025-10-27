from PIL import Image
img = Image.open("recovered.png").convert("L")
threshold = 200
w,h = img.size
for y in range(0,h,4):
    line = []
    for x in range(0,w,4):
        block = img.crop((x,y,x+4,y+4))
        avg = sum(block.getdata())/len(block.getdata())
        line.append('#' if avg < threshold else ' ')
    print(''.join(line))
