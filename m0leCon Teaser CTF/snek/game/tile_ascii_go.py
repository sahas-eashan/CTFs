from PIL import Image

img = Image.open("remote_gameover.png").convert("L")
arr = img.load()

chars = {True:'#', False:'.'}

def print_tile(tx, ty, thr=150):
    print(f"Tile ({tx},{ty})")
    for y in range(ty*20, ty*20+20):
        row = ''.join('#' if arr[x, y] < thr else '.' for x in range(tx*20, tx*20+20))
        print(row)
    print()

# Print tiles for scoreboard and game over text
for ty in [0,1,7,8]:
    for tx in range(10):
        print_tile(tx, ty)
