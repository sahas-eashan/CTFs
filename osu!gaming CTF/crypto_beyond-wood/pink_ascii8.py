from PIL import Image
img = Image.open("recovered.png").crop((70,65,456,245))
pink = (255,174,200)
scale = 8
w,h = img.size
for y in range(0,h,scale):
    line = []
    for x in range(0,w,scale):
        block = img.crop((x,y,x+scale,y+scale))
        data = block.getdata()
        cnt = sum(1 for p in data if p == pink)
        line.append('X' if cnt > len(data)//3 else ' ')
    if any(c == 'X' for c in line):
        print(''.join(line))
