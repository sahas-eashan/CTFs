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
    h,w=region.shape
    print('char',idx,'shape',h,w)
    for row in region:
        print(''.join('#' if v else ' ' for v in row))
    print()
