from PIL import Image, ImageDraw, ImageFilter
import numpy as np

def process():
    orig_path = 'public/mockups/macbook_new.png'
    out_path = 'public/mockups/macbook_8k.png'
    
    orig = Image.open(orig_path).convert('RGBA')
    w_orig, h_orig = orig.size
    scale = 4
    w_4k, h_4k = w_orig * scale, h_orig * scale
    
    print("Edge padding RGB...")
    # Fill the inner hole with Black, so it doesn't bleed white.
    bg = Image.new('RGBA', orig.size, (0,0,0,0))
    draw = ImageDraw.Draw(bg)
    draw.rectangle([110, 12, 913, 525], fill=(0,0,0,255))
    orig_filled = Image.alpha_composite(bg, orig)
    
    # Solidify the outer edges to prevent dark halos
    arr = np.array(orig_filled)
    rgb = arr[:,:,0:3]
    alpha_arr = np.array(orig.split()[3])
    mask_arr = alpha_arr > 0
    
    current_rgb = Image.fromarray(rgb, 'RGB')
    for i in range(16):
        blurred = current_rgb.filter(ImageFilter.BoxBlur(1))
        blurred_arr = np.array(blurred)
        rgb_arr = np.array(current_rgb)
        rgb_arr[~mask_arr] = blurred_arr[~mask_arr]
        current_rgb = Image.fromarray(rgb_arr, 'RGB')
        
    print("Upscaling RGB...")
    rgb_4k = current_rgb.resize((w_4k, h_4k), resample=Image.LANCZOS)
    
    print("Redrawing mathematically perfect SSAA Mask at 16K...")
    ssaa = 4
    w_16k, h_16k = w_4k * ssaa, h_4k * ssaa
    mask_16k = Image.new("L", (w_16k, h_16k), 0)
    draw_16k = ImageDraw.Draw(mask_16k)
    
    def box(x1, y1, x2, y2):
        return [x1 * scale * ssaa, y1 * scale * ssaa, x2 * scale * ssaa, y2 * scale * ssaa]
        
    # Base bounding box for the entire image is 0. 
    # But we want to preserve the bottom base of the laptop exactly as it is, because it's complex geometry.
    # So we will ONLY draw the mask for the top half (y < 300), and use the original alpha for the bottom half!
    # Wait, the user complained about the corners. The top corners are the only ones visible for the lid.
    
    # Actually, drawing the whole thing is safer and cleaner if we match it well.
    # Let's draw the whole outer lid.
    # The laptop lid is x=98 to x=926.
    lid_box = box(98, 0, 926, 600) # extending past the bottom
    lid_radius = 24 * scale * ssaa
    draw_16k.rounded_rectangle(lid_box, radius=lid_radius, fill=255)
    
    # Subtract the inner hole
    hole_box = box(110, 12, 913, 525)
    hole_radius = 10 * scale * ssaa
    draw_16k.rounded_rectangle(hole_box, radius=hole_radius, fill=0)
    
    # Add back the notch
    notch_box = box(469, 0, 555, 27) # start from y=0 to overlap completely
    notch_radius = 6 * scale * ssaa
    draw_16k.rounded_rectangle(notch_box, radius=notch_radius, fill=255)
    
    print("Downsampling 16K mask to 4K...")
    mask_4k_drawn = mask_16k.resize((w_4k, h_4k), resample=Image.LANCZOS)
    
    # We must preserve the bottom half of the original alpha (the keyboard base and drop shadow).
    # The hinge is at y=525. So from y=525 downwards, we use the original upscaled alpha.
    print("Merging drawn mask with original bottom mask...")
    orig_alpha_4k = orig.split()[3].resize((w_4k, h_4k), resample=Image.LANCZOS)
    
    # Create a vertical gradient mask to blend the two masks seamlessly
    blend = Image.new("L", (w_4k, h_4k), 0)
    blend_draw = ImageDraw.Draw(blend)
    # y=500 is 100% drawn mask (white). y=530 is 100% original mask (black).
    blend_draw.rectangle([0, 0, w_4k, 500 * scale], fill=255)
    for y in range(500 * scale, 530 * scale):
        opacity = int(255 * (1 - (y - 500 * scale) / (30 * scale)))
        blend_draw.line([(0, y), (w_4k, y)], fill=opacity)
        
    final_mask = Image.composite(mask_4k_drawn, orig_alpha_4k, blend)
    
    print("Saving final flawless PNG...")
    rgb_4k.putalpha(final_mask)
    rgb_4k.save(out_path)
    print("Done!")

process()
