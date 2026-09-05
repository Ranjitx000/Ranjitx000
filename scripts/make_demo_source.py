"""
Generates a demo grayscale 'portrait' (a stylized terminal/robot face) so the
ASCII pipeline can be demoed without a real photo. Replace this step with
prep_photo.py + your own photo when you're ready to use your face instead.
"""
from PIL import Image, ImageDraw
import numpy as np

W, H = 480, 480
img = Image.new("L", (W, H), color=255)
d = ImageDraw.Draw(img)

cx, cy = W // 2, H // 2

# Head (rounded square, gives clean ascii edges)
d.rounded_rectangle([cx-150, cy-170, cx+150, cy+150], radius=40, fill=40)

# Visor / eyes band
d.rounded_rectangle([cx-115, cy-70, cx+115, cy+10], radius=24, fill=230)

# Eyes
d.ellipse([cx-80, cy-45, cx-25, cy-5], fill=25)
d.ellipse([cx+25, cy-45, cx+80, cy-5], fill=25)

# Eye glow (bright ascii will punch through as sparse chars)
d.ellipse([cx-65, cy-35, cx-40, cy-15], fill=250)
d.ellipse([cx+40, cy-35, cx+65, cy-15], fill=250)

# Mouth grille
for i in range(5):
    x0 = cx - 60 + i * 30
    d.rounded_rectangle([x0, cy+55, x0+18, cy+90], radius=4, fill=210)

# Antenna
d.line([cx, cy-170, cx, cy-210], fill=40, width=10)
d.ellipse([cx-16, cy-230, cx+16, cy-198], fill=245)

# Shoulders
d.rounded_rectangle([cx-190, cy+140, cx+190, cy+230], radius=30, fill=60)

img.save("demo-source.png")
print("wrote demo-source.png")
