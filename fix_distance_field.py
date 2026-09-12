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
    
    # Extract Alpha and create Binary Mask
    alpha = np.array(orig.split()[3])
    mask = alpha > 127
    
    print("Computing Signed Distance Field (SDF)...")
    # Distance to the nearest True pixel (inside the mask, distance is 0)
    # Distance to the nearest False pixel (outside the mask, distance is 0)
    # We want exact signed distance: positive inside, negative outside.
    dist_inside = ndimage.distance_transform_edt(mask)
    dist_outside = ndimage.distance_transform_edt(~mask)
    
    # SDF: >0 inside, <0 outside
    # Subtract 0.5 to center the edge perfectly between pixels
    sdf = dist_inside - dist_outside
    
    print("Upscaling SDF using High-Quality Bicubic Interpolation...")
    # Convert SDF to a float image and resize
    # PIL can resize float32 images!
    sdf_img = Image.fromarray(sdf.astype(np.float32), mode='F')
    sdf_4k = sdf_img.resize(new_size, resample=Image.BICUBIC)
    
    # Convert back to numpy
    sdf_4k_arr = np.array(sdf_4k)
    
    print("Generating perfect anti-aliased Alpha mask from 4K SDF...")
    # In the 4K image, 1 pixel is 0.25 units in the original SDF.
    # To get a 1-pixel wide anti-aliased edge at 4K scale, we map SDF from -0.5 to 0.5?
    # Actually, the SDF values in sdf_4k_arr are in *original 1024px* units.
    # So 1 pixel in the 4K image is 0.25 units.
    # An anti-aliased edge should transition over 1 to 1.5 pixels in the 4K image.
    # So the transition window in SDF units is roughly -0.2 to +0.2.
    
    # Let's map SDF = -0.2 to 0, and SDF = +0.2 to 255.
    # new_alpha = np.clip((sdf_4k_arr + 0.25) / 0.5, 0, 1) * 255
    # Wait, the edge in the original mask is at exactly 0.
    # To match the original, and prevent it from shrinking/growing, the center of the transition must be 0.
    # width of transition = 0.5 SDF units (which is 2 pixels in 4K).
    transition_width = 0.5 
    new_alpha_arr = np.clip((sdf_4k_arr + transition_width/2) / transition_width, 0, 1) * 255
    new_alpha_img = Image.fromarray(new_alpha_arr.astype(np.uint8), mode='L')
    
    # Solidify RGB
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
        
    print("Upscaling RGB...")
    rgb_4k = current_rgb.resize(new_size, resample=Image.LANCZOS)
    
    print("Merging flawless SDF mask with padded RGB...")
    rgb_4k.putalpha(new_alpha_img)
    rgb_4k.save(out_path)
    
    # Verifying the generated PNG by checking an edge pixel
    alpha_check = rgb_4k.split()[3]
    print(f"Flawless organic 4K mockup generated. Edge check: {alpha_check.getpixel((440, 200))}")

process()
