from PIL import Image
img = Image.open("remote.png")
score = img.crop((20, 0, 180, 40))
score.save("score.png")
print("saved score.png")
