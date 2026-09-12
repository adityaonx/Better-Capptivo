from PIL import Image, ImageFilter
import numpy as np

def process():
    orig = Image.open('public/mockups/macbook_new.png').convert('RGBA')
    w, h = orig.size
    
    # 1. Fill inner hole with Black (since the inner bezel is always black)
    # We can just draw a black rectangle for the inner hole
    bg = Image.new('RGBA', orig.size, (0,0,0,0))
    from PIL import ImageDraw
    draw = ImageDraw.Draw(bg)
    draw.rectangle([110, 12, 913, 525], fill=(0,0,0,255))
    orig = Image.alpha_composite(bg, orig)
    
    # 2. True Solidify (Edge Padding) for the outside
    print("Solidifying edges...")
    # Convert to numpy for fast processing
    arr = np.array(orig)
    rgb = arr[:,:,0:3]
    alpha = arr[:,:,3]
    
    # We want to iteratively grow the RGB colors into areas where alpha == 0
    # A simple way: blur the RGB, and where alpha == 0, replace with blurred RGB.
    # Repeat this 10 times to push the colors outwards by ~10 pixels.
    # We use PIL for the blur.
    
    current_rgb = Image.fromarray(rgb, 'RGB')
    mask_arr = alpha > 0
    
    for i in range(16):
        # Blur the current rgb
        blurred = current_rgb.filter(ImageFilter.BoxBlur(1))
        blurred_arr = np.array(blurred)
        
        # Replace only the transparent pixels
        rgb_arr = np.array(current_rgb)
        rgb_arr[~mask_arr] = blurred_arr[~mask_arr]
        current_rgb = Image.fromarray(rgb_arr, 'RGB')
        
        # Expand the mask by 1 pixel so the newly colored pixels can bleed further
        # Actually, box blur spreads colors anyway. But we keep the original mask 
        # so we don't degrade the original opaque pixels.
        
    print("Solidify complete.")
    
    # 3. Upscale RGB
    scale = 4
    new_size = (w * scale, h * scale)
    print("Upscaling RGB with Lanczos...")
    rgb_4k = current_rgb.resize(new_size, resample=Image.LANCZOS)
    
    # 4. Upscale Alpha with Contrast Curve
    print("Upscaling Alpha...")
    alpha_img = Image.fromarray(alpha, 'L')
    alpha_4k_soft = alpha_img.resize(new_size, resample=Image.LANCZOS)
    
    min_val = 96
    max_val = 160
    rng = max_val - min_val
    def contrast(p):
        if p <= min_val: return 0
        if p >= max_val: return 255
        return int((p - min_val) / rng * 255)
        
    alpha_4k_sharp = alpha_4k_soft.point(contrast)
    
    # 5. Merge
    print("Merging...")
    rgb_4k.putalpha(alpha_4k_sharp)
    rgb_4k.save('public/mockups/macbook_8k.png')
    print("Flawless organic 4K mockup generated.")

process()
