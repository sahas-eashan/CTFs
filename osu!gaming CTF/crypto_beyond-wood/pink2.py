from PIL import Image
img = Image.open("recovered.png")
pink = (255,174,200)
scale = 6
w,h = img.size
for y in range(0,h,scale):
    line = []
    for x in range(0,w,scale):
        block = img.crop((x,y,x+scale,y+scale))
        data = block.getdata()
        count = sum(1 for p in data if p == pink)
        line.append('#' if count > len(data)//2 else ' ')
    if any(c == '#' for c in line):
        print(''.join(line))
