import sys
import os
from PIL import Image, ImageEnhance, ImageDraw, ImageChops

def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def apply_choso_effect(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: Could not find '{input_path}'. Please ensure the photo is saved in the directory.")
        sys.exit(1)

    print(f"Loading {input_path}...")
    img = Image.open(input_path).convert("RGB")
    
    # --- 1. Preprocessing ---
    # Brightness: -16 (scale from 1.0)
    brightness_factor = 1.0 - (16.0 / 100.0)
    img = ImageEnhance.Brightness(img).enhance(brightness_factor)
    
    # Contrast: 100 (assume 100 means max boost, so a factor of 2.0)
    contrast_factor = 2.0
    img = ImageEnhance.Contrast(img).enhance(contrast_factor)
    
    # Grayscale: 100
    img = img.convert("L")
    
    w, h = img.size
    
    # --- 2. Grid & Dithering ---
    cell_size = 9
    tint = hex_to_rgb("#9d00ff")
    
    # Create the output canvas (black background since bgMode=none)
    out_img = Image.new("RGB", (w, h), (0, 0, 0))
    draw = ImageDraw.Draw(out_img)
    
    # Bayer 4x4 matrix mapped to 0-255 scale
    bayer = [
        [ 0,  8,  2, 10],
        [12,  4, 14,  6],
        [ 3, 11,  1,  9],
        [15,  7, 13,  5]
    ]
    
    print("Applying Bayer Dither (cell_size=9)...")
    for cy in range(0, h, cell_size):
        for cx in range(0, w, cell_size):
            # Sample luminance by taking the center pixel of the cell
            # (or we could average the cell, but center pixel is faster and often sharper for dithering)
            sample_x = min(cx + cell_size // 2, w - 1)
            sample_y = min(cy + cell_size // 2, h - 1)
            lum = img.getpixel((sample_x, sample_y))
            
            # Get bayer threshold
            grid_x = cx // cell_size
            grid_y = cy // cell_size
            # Normalize bayer to 0-255 (multiply by 16)
            threshold = (bayer[grid_y % 4][grid_x % 4] + 0.5) * 16.0
            
            # If luminance passes threshold, draw the primitive (a solid rectangle)
            if lum > threshold:
                draw.rectangle([cx, cy, cx + cell_size - 1, cy + cell_size - 1], fill=tint)
                
    # --- 3. Post-Effects (PFX) ---
    # Chromatic aberration (intensity 15)
    print("Applying Chromatic Aberration...")
    intensity = 15
    shift = max(1, intensity // 5)  # roughly 3 pixels shift
    
    r, g, b = out_img.split()
    r = ImageChops.offset(r, -shift, 0)
    b = ImageChops.offset(b, shift, 0)
    final_img = Image.merge("RGB", (r, g, b))
    
    final_img.save(output_path)
    print(f"Success! Saved CHOSO ASCII effect to {output_path}")

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "photo.jpg"
    out = sys.argv[2] if len(sys.argv) > 2 else "choso-output.png"
    apply_choso_effect(src, out)
