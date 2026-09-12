import numpy as np
from scipy import ndimage
from PIL import Image, ImageFilter

def process():
    orig_path = 'public/mockups/macbook_new.png'
    out_path = 'public/mockups/macbook_8k.png'
    
    orig = Image.open(orig_path).convert('RGBA')
    w, h = orig.size
    scale = 4
    new_size = (w * scale, h * scale)
    
    alpha = np.array(orig.split()[3])
    mask = alpha > 127
    
    dist_inside = ndimage.distance_transform_edt(mask)
    dist_outside = ndimage.distance_transform_edt(~mask)
    
    sdf = dist_inside - dist_outside
    # Fix the zero-crossing gradient!
    sdf[sdf > 0] -= 0.5
    sdf[sdf < 0] += 0.5
    
    sdf_img = Image.fromarray(sdf.astype(np.float32), mode='F')
    sdf_4k = sdf_img.resize(new_size, resample=Image.BICUBIC)
    sdf_4k_arr = np.array(sdf_4k)
    
    # Transition width of 0.5 to 0.75 SDF units creates a beautiful 2-3 pixel anti-aliasing
    transition_width = 0.75 
    new_alpha_arr = np.clip((sdf_4k_arr + transition_width/2) / transition_width, 0, 1) * 255
    new_alpha_img = Image.fromarray(new_alpha_arr.astype(np.uint8), mode='L')
    
    print("Edge padding RGB...")
    bg = Image.new('RGBA', orig.size, (0,0,0,0))
    from PIL import ImageDraw
    draw = ImageDraw.Draw(bg)
    draw.rectangle([110, 12, 913, 525], fill=(0,0,0,255))
    orig_filled = Image.alpha_composite(bg, orig)
    
    arr = np.array(orig_filled)
    rgb = arr[:,:,0:3]
    mask_arr = alpha > 0
    current_rgb = Image.fromarray(rgb, 'RGB')
    
    for i in range(16):
        blurred = current_rgb.filter(ImageFilter.BoxBlur(1))
        blurred_arr = np.array(blurred)
        rgb_arr = np.array(current_rgb)
        rgb_arr[~mask_arr] = blurred_arr[~mask_arr]
        current_rgb = Image.fromarray(rgb_arr, 'RGB')
        
    rgb_4k = current_rgb.resize(new_size, resample=Image.LANCZOS)
    
    rgb_4k.putalpha(new_alpha_img)
    rgb_4k.save(out_path)
    
    # Verify the edge gradient!
    alpha_4k = np.array(new_alpha_img)
    print("Edge check at y=200, scanning x=440 to 455:")
    for x in range(440, 455):
        print(f"x={x}: {alpha_4k[200, x]}")

process()
