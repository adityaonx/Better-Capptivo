from PIL import Image, ImageFilter
import numpy as np

def process():
    orig_path = 'public/mockups/macbook_new.png'
    out_path = 'public/mockups/macbook_8k.png'
    
    orig = Image.open(orig_path).convert('RGBA')
    w, h = orig.size
    scale = 4
    new_size = (w * scale, h * scale)
    
    # Extract pristine original alpha
    original_alpha = orig.split()[3]
    
    # Fill inner hole with Black to prevent color bleeding
    bg = Image.new('RGBA', orig.size, (0,0,0,0))
    from PIL import ImageDraw
    draw = ImageDraw.Draw(bg)
    draw.rectangle([110, 12, 913, 525], fill=(0,0,0,255))
    orig_filled = Image.alpha_composite(bg, orig)
    
    # Solidify (Edge Pad) the RGB to prevent outer halos
    arr = np.array(orig_filled)
    rgb = arr[:,:,0:3]
    alpha_arr = np.array(original_alpha)
    mask_arr = alpha_arr > 0
    current_rgb = Image.fromarray(rgb, 'RGB')
    
    for i in range(16):
        blurred = current_rgb.filter(ImageFilter.BoxBlur(1))
        blurred_arr = np.array(blurred)
        rgb_arr = np.array(current_rgb)
        rgb_arr[~mask_arr] = blurred_arr[~mask_arr]
        current_rgb = Image.fromarray(rgb_arr, 'RGB')
        
    print("Upscaling RGB with high-quality Lanczos...")
    rgb_4k = current_rgb.resize(new_size, resample=Image.LANCZOS)
    
    print("Upscaling Alpha with high-quality Lanczos (preserving exact squircle geometry)...")
    # NO contrast curve! Let Lanczos provide a beautifully smooth, natural anti-aliased gradient!
    alpha_4k = original_alpha.resize(new_size, resample=Image.LANCZOS)
    
    print("Merging...")
    rgb_4k.putalpha(alpha_4k)
    rgb_4k.save(out_path)
    print("Perfect organic 4K mockup generated.")

process()
