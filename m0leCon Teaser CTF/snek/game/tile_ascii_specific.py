from PIL import Image

img = Image.open("remote_gameover.png").convert("L")
arr = img.load()

def print_tile(tx, ty, thr=160):
    print(f"Tile ({tx},{ty})")
    for y in range(ty*20, ty*20+20):
        print(''.join('#' if arr[x, y] < thr else '.' for x in range(tx*20, tx*20+20)))
    print()

tiles = [(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),(8,7),(9,7),
         (0,8),(1,8),(2,8),(3,8),(4,8),(5,8),(6,8),(7,8),(8,8),(9,8)]
for tx, ty in tiles:
    print_tile(tx, ty)
