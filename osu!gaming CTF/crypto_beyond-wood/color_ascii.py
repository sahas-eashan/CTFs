from PIL import Image
img = Image.open("recovered.png").crop((70,65,456,245))
color = (73,63,52)
scale = 6
w,h = img.size
for y in range(0,h,scale):
    line=[]
    for x in range(0,w,scale):
        block = img.crop((x,y,x+scale,y+scale))
        data = block.getdata()
        cnt = sum(1 for p in data if p == color)
        line.append('#' if cnt > len(data)//2 else ' ')
    if any(c=='#' for c in line):
        print(''.join(line))
