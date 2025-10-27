from PIL import Image
img = Image.open("recovered.png").convert("L")
scale = 4
w,h = img.size
for y in range(0,h,scale):
    line = []
    for x in range(0,w,scale):
        block = img.crop((x,y,x+scale,y+scale))
        avg = sum(block.getdata())/len(block.getdata())
        line.append(' ' if avg > 200 else '#')
    if any(c == '#' for c in line):
        print(''.join(line))
