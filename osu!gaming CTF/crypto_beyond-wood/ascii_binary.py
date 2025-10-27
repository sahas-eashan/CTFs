from PIL import Image
img = Image.open("binary.png")
chars = " @#"
w,h = img.size
new_w = 120
new_h = max(1, int(h * new_w / w / 2))
img = img.resize((new_w, new_h))
for y in range(new_h):
    line = ''.join(chars[p//128*2] if p else '#' for p in img.crop((0,y,new_w,y+1)).getdata())
    print(line)
