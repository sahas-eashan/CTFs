from PIL import Image

img = Image.open("remote_gameover.png").convert("L")
arr = img.load()

def print_letter(tx, ty, thr=128):
    print(f"Tile ({tx},{ty})")
    for y in range(ty*20, ty*20+20):
        line = ''.join('#' if arr[x, y] < thr else ' ' for x in range(tx*20, tx*20+20))
        print(line)
    print()

for tx in range(10):
    print_letter(tx, 0)
