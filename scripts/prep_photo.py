"""
Prepares a real photo for the ASCII pipeline:
  1. Remove the background (rembg) so only the subject remains.
  2. Boost local contrast with CLAHE so a flatly-lit face still reads with
     highlights and shadows once it's down-sampled to a character grid.
  3. Composite onto pure white so the background maps to blank ascii chars.

Usage: python prep_photo.py your-photo.jpg
Output: prepped-source.png  (feed this into make_ascii_svg.py)
"""
import sys

import cv2
import numpy as np
from PIL import Image
from rembg import remove

SRC = sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg"
OUT = sys.argv[2] if len(sys.argv) > 2 else "prepped-source.png"


def main():
    with open(SRC, "rb") as f:
        input_bytes = f.read()
    cutout = remove(input_bytes)  # RGBA, background removed

    img = Image.open(__import__("io").BytesIO(cutout)).convert("RGBA")
    white_bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    composited = Image.alpha_composite(white_bg, img).convert("L")

    arr = np.array(composited)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    boosted = clahe.apply(arr)

    Image.fromarray(boosted).save(OUT)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
