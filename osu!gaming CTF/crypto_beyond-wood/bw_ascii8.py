from PIL import Image
img = Image.open("recovered.png").crop((70,65,456,245)).convert("L")
scale = 8
w,h = img.size
for y in range(0,h,scale):
    line = []
    for x in range(0,w,scale):
        block = img.crop((x,y,x+scale,y+scale))
        avg = sum(block.getdata())/len(block.getdata())
        line.append('X' if avg < 230 else ' ')
    if any(c == 'X' for c in line):
        print(''.join(line))
