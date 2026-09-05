import sys
import os
import math
from PIL import Image, ImageEnhance, ImageDraw, ImageChops

def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def generate_choso_gif(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: Could not find '{input_path}'. Please ensure the photo is saved in the directory.")
        sys.exit(1)

    print(f"Loading {input_path}...")
    img = Image.open(input_path).convert("RGB")
    
    # --- 1. Preprocessing ---
    brightness_factor = 1.0 - (16.0 / 100.0)
    img = ImageEnhance.Brightness(img).enhance(brightness_factor)
    contrast_factor = 2.0
    img = ImageEnhance.Contrast(img).enhance(contrast_factor)
    img = img.convert("L")
    w, h = img.size
    
    cell_size = 9
    tint = hex_to_rgb("#9d00ff")
    
    bayer = [
        [ 0,  8,  2, 10],
        [12,  4, 14,  6],
        [ 3, 11,  1,  9],
        [15,  7, 13,  5]
    ]
    
    frames = []
    total_frames = 24
    
    print(f"Rendering {total_frames} frames for animation...")
    for frame in range(total_frames):
        out_img = Image.new("RGB", (w, h), (0, 0, 0))
        draw = ImageDraw.Draw(out_img)
        
        # Pulse animation (uniform oscillation over time, slightly delayed radially)
        # animIntensity: 41, animSpeed: 64
        # We'll use a sine wave that completes 1 full cycle over the 24 frames
        time_t = (frame / total_frames) * math.pi * 2
        
        for cy in range(0, h, cell_size):
            for cx in range(0, w, cell_size):
                sample_x = min(cx + cell_size // 2, w - 1)
                sample_y = min(cy + cell_size // 2, h - 1)
                lum = img.getpixel((sample_x, sample_y))
                
                grid_x = cx // cell_size
                grid_y = cy // cell_size
                threshold = (bayer[grid_y % 4][grid_x % 4] + 0.5) * 16.0
                
                if lum > threshold:
                    # Calculate spatial phase for the pulse (ripple from center)
                    dx = cx - (w / 2)
                    dy = cy - (h / 2)
                    dist = math.sqrt(dx*dx + dy*dy)
                    phase = dist * 0.015
                    
                    oscillation = math.sin(time_t - phase)
                    # Modulate rect size between 50% and 100% of cell_size
                    rect_s = cell_size * (0.75 + 0.25 * oscillation)
                    offset = (cell_size - rect_s) / 2
                    
                    draw.rectangle(
                        [cx + offset, cy + offset, cx + cell_size - 1 - offset, cy + cell_size - 1 - offset], 
                        fill=tint
                    )
                    
        # Post-Effects (PFX) - Chromatic aberration
        intensity = 15
        shift = max(1, intensity // 5)
        
        r, g, b = out_img.split()
        r = ImageChops.offset(r, -shift, 0)
        b = ImageChops.offset(b, shift, 0)
        final_img = Image.merge("RGB", (r, g, b))
        
        frames.append(final_img)
        sys.stdout.write(f"\rRendered frame {frame+1}/{total_frames}")
        sys.stdout.flush()
        
    print("\nSaving GIF...")
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=1000 // 24, # 24 fps
        loop=0
    )
    print(f"Success! Saved Animated CHOSO effect to {output_path}")

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "photo.jpg"
    out = sys.argv[2] if len(sys.argv) > 2 else "choso-animated.gif"
    generate_choso_gif(src, out)
