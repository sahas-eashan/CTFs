from PIL import Image
uns=Image.open("unscrambled.png")
rec=Image.open("recovered.png")
width,height=uns.size
for i in range(width):
    for j in range(height):
        u=uns.getpixel((i,j))
        r=rec.getpixel((i,j))
        k=tuple(u[x]^r[x] for x in range(3))
        if k != (0,0,0):
            print(k)
            raise SystemExit
