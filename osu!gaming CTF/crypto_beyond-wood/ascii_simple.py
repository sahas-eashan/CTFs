from PIL import Image
chars = " @#"
img = Image.open("recovered.png").convert("L")
w,h = img.size
new_w = 80
new_h = max(1, int(h * new_w / w / 2))
img = img.resize((new_w, new_h))
for y in range(new_h):
    line = ''.join(chars[int(p * len(chars) / 256)] for p in img.crop((0, y, new_w, y + 1)).getdata())
    print(line)
