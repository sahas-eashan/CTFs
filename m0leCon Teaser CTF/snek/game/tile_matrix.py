from PIL import Image

img = Image.open("remote_gameover.png").convert("L")
arr = img.load()

def print_matrix(tx, ty):
    for y in range(ty*20, ty*20+20):
        line = ''.join('1' if arr[x,y] > 128 else '0' for x in range(tx*20, tx*20+20))
        print(line)
    print()

print('Tile (0,0)')
print_matrix(0,0)
print('Tile (9,0)')
print_matrix(9,0)
