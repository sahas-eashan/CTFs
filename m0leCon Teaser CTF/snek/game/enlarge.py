from PIL import Image
img = Image.open("score.png").convert("L")
img = img.resize((img.width*2, img.height*2), Image.NEAREST)
img.save("score_scaled.png")
