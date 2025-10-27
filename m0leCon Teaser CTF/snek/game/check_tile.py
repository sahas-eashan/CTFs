from PIL import Image

img = Image.open("remote_gameover.png")
pixels = img.load()

def stats(tx, ty):
    total = [0,0,0]
    for y in range(ty*20, ty*20+20):
        for x in range(tx*20, tx*20+20):
            r,g,b = pixels[x,y][:3]
            total[0] += r
            total[1] += g
            total[2] += b
    avg = [t/400 for t in total]
    print((tx,ty), avg)

for coord in [(3,4),(4,4),(5,4),(6,4),(3,5),(4,5),(5,5),(6,5)]:
    stats(*coord)
