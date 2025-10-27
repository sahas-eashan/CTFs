from PIL import Image

img = Image.open("remote_gameover.png").convert("L")
arr = img.load()

thr = 200
for ty in range(10):
    for tx in range(10):
        block_mean = sum(arr[tx*20 + x, ty*20 + y] for x in range(20) for y in range(20)) / 400
        if block_mean >= 240:
            continue
        print(f"Tile ({tx},{ty}) mean {block_mean:.1f}")
        for y in range(ty*20, ty*20+20):
            row = ''.join('#' if arr[x, y] < 180 else '.' for x in range(tx*20, tx*20+20))
            print(row)
        print()
