from PIL import Image
img = Image.open("remote.png")
print(img.size, img.mode)
