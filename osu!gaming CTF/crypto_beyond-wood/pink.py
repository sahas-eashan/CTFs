from PIL import Image
img = Image.open("recovered.png")
w,h = img.size
for y in range(0,h,4):
    line = []
    for x in range(0,w,2):
        pixel = img.getpixel((x,y))
        if pixel == (255, 174, 200):
            line.append('#')
        else:
            line.append(' ')
    if any(c == '#' for c in line):
        print(''.join(line))
