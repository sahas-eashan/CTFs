from PIL import Image
import numpy as np
img = Image.open("remote_gameover.png").convert('L')
arr = np.array(img)
for coord in [(3,4),(4,4),(5,4),(6,4)]:
    tile = arr[coord[1]*20:(coord[1]+1)*20, coord[0]*20:(coord[0]+1)*20]
    mean = tile.mean()
    print(coord, mean, tile.max(), tile.min())
