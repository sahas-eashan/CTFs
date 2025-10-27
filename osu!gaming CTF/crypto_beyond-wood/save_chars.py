import numpy as np
from PIL import Image
img=Image.open("crop_ext0_erode.png")
bin_img=(np.array(img)<128).astype(np.uint8)
segments=[(49,84),(91,167),(173,229),(232,259),(263,285),(293,332),(337,390),(399,423)]
for idx,(x1,x2) in enumerate(segments):
    region=bin_img[:,x1:x2]
    rows=np.where(region.sum(axis=1)>0)[0]
    y1,y2=rows[0],rows[-1]+1
    region=region[y1:y2,:]
    Image.fromarray(region*255).resize((region.shape[1]*6, region.shape[0]*6), Image.NEAREST).save(f'char_{idx}.png')
