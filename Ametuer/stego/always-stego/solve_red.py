from PIL import Image
import numpy as np

# load image
img = Image.open("output.png")
arr = np.array(img)
red = arr[:,:,0].flatten()

# histogram
hist = np.bincount(red, minlength=256)

# sort intensities by frequency
order_asc = np.argsort(hist)
even_vals = [i for i in range(256) if i % 2 == 0]

# positions of even intensities in sorted histogram
positions_even_in_asc = [
    int(np.where(order_asc == e)[0][0]) for e in even_vals
]
pe = bytes(positions_even_in_asc)

print("positions_even_in_asc length:", len(pe))
print("raw bytes:", pe)
print("latin-1:", pe.decode("latin-1", errors="replace"))

# extract the nice ASCII run manually once you see it printed:
# }hadp`NQCH6LFD;R?J4EB<UusVfigZ[cn]xz
