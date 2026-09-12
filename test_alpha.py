from PIL import Image

def process():
    orig = Image.open('public/mockups/macbook_new.png').convert('RGBA')
    alpha = orig.split()[3]
    
    scale = 4
    w, h = orig.size
    new_size = (w * scale, h * scale)
    
    print("Upscaling alpha with Lanczos (soft)...")
    alpha_4k_soft = alpha.resize(new_size, resample=Image.LANCZOS)
    
    print("Applying contrast curve (Distance Field sharpening)...")
    # We want to compress the transition.
    # Center is 128. Let's use a window of +/- 32. So 96 to 160.
    # This compresses a ~8 pixel blur into a ~2 pixel blur, making it crisp but anti-aliased.
    min_val = 96
    max_val = 160
    rng = max_val - min_val
    
    def contrast(p):
        if p <= min_val: return 0
        if p >= max_val: return 255
        return int((p - min_val) / rng * 255)
        
    alpha_4k_sharp = alpha_4k_soft.point(contrast)
    
    print("Edge-padding RGB...")
    # Grey background outside, Black background inside
    bg = Image.new('RGBA', orig.size, (140, 142, 145, 255))
    from PIL import ImageDraw
    draw = ImageDraw.Draw(bg)
    draw.rectangle([110, 12, 913, 525], fill=(0,0,0,255))
    
    rgb_filled = Image.alpha_composite(bg, orig).convert('RGB')
    
    print("Upscaling RGB with Lanczos...")
    rgb_4k = rgb_filled.resize(new_size, resample=Image.LANCZOS)
    
    print("Merging...")
    rgb_4k.putalpha(alpha_4k_sharp)
    
    rgb_4k.save('public/mockups/macbook_8k.png')
    print("Flawless organic 4K mockup generated.")

process()
