from PIL import Image
img = Image.open("recovered.png").crop((70,65,456,245))
img = img.convert("L")
chars = " @#"
new_w = 80
new_h = max(1, int(img.height * new_w / img.width / 2))
img = img.resize((new_w,new_h))
for y in range(new_h):
    line = ''.join(chars[int(p * len(chars) / 256)] for p in img.crop((0,y,new_w,y+1)).getdata())
    print(line)
