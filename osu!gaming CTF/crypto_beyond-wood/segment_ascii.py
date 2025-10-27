import numpy as np
from PIL import Image
img=Image.open("crop_ext0_erode.png")
bin_img=(np.array(img)<128).astype(int)
segments=[(49,84),(91,167),(173,229),(232,259),(263,285),(293,332),(337,390),(399,423)]
for idx,(x1,x2) in enumerate(segments):
    region=bin_img[:,x1:x2]
    rows=np.where(region.sum(axis=1)>0)[0]
    y1,y2=rows[0],rows[-1]+1
    region=region[y1:y2,:]
    print('char',idx,'size',region.shape)
    for y in range(0,region.shape[0], max(1,region.shape[0]//12)):
        row=''.join('#' if region[y,x] else ' ' for x in range(0,region.shape[1], max(1,region.shape[1]//24)))
        print(row)
    print()
