from PIL import Image
img = Image.open("recovered.png")
w,h = img.size
nonwhite = []
for y in range(h):
    for x in range(w):
        if img.getpixel((x,y)) != (255,255,255):
            nonwhite.append((x,y))
if not nonwhite:
    print("all white")
    raise SystemExit
xs = [x for x,_ in nonwhite]
ys = [y for _,y in nonwhite]
print(min(xs), max(xs), min(ys), max(ys))
