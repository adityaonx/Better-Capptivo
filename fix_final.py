from PIL import Image, ImageFilter
import numpy as np

def process():
    orig_path = 'public/mockups/macbook_new.png'
    out_path = 'public/mockups/macbook_8k.png'
    
    orig = Image.open(orig_path).convert('RGBA')
    w, h = orig.size
    
    # 1. EXTRACT ORIGINAL ALPHA BEFORE ANY COMPOSITING
    original_alpha = orig.split()[3]
    
    # 2. Prepare RGB for Edge Padding (Solidify)
    # Fill the inner hole with Black, so that it blends into Black during upscale
    bg = Image.new('RGBA', orig.size, (0,0,0,0))
    from PIL import ImageDraw
    draw = ImageDraw.Draw(bg)
    draw.rectangle([110, 12, 913, 525], fill=(0,0,0,255))
    orig_filled = Image.alpha_composite(bg, orig)
    
    # Convert to numpy for fast processing
    arr = np.array(orig_filled)
    rgb = arr[:,:,0:3]
    
    # We use the original alpha to mask the edge padding!
    alpha_arr = np.array(original_alpha)
    
    print("Solidifying edges...")
    current_rgb = Image.fromarray(rgb, 'RGB')
    mask_arr = alpha_arr > 0
    
    for i in range(16):
        blurred = current_rgb.filter(ImageFilter.BoxBlur(1))
        blurred_arr = np.array(blurred)
        
        rgb_arr = np.array(current_rgb)
        rgb_arr[~mask_arr] = blurred_arr[~mask_arr]
        current_rgb = Image.fromarray(rgb_arr, 'RGB')
        
    # 3. Upscale RGB
    scale = 4
    new_size = (w * scale, h * scale)
    rgb_4k = current_rgb.resize(new_size, resample=Image.LANCZOS)
    
    # 4. Upscale Original Alpha with Contrast Curve
    alpha_4k_soft = original_alpha.resize(new_size, resample=Image.LANCZOS)
    
    min_val = 96
    max_val = 160
    rng = max_val - min_val
    def contrast(p):
        if p <= min_val: return 0
        if p >= max_val: return 255
        return int((p - min_val) / rng * 255)
        
    alpha_4k_sharp = alpha_4k_soft.point(contrast)
    
    # 5. Merge
    rgb_4k.putalpha(alpha_4k_sharp)
    rgb_4k.save(out_path)
    print("Flawless organic 4K mockup with TRANSPARENT HOLE generated.")

process()
