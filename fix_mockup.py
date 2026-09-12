import sys
from PIL import Image, ImageFilter, ImageDraw

def process():
    # Open the original 1024x594 PNG
    orig = Image.open('public/mockups/macbook_new.png').convert('RGBA')
    w, h = orig.size
    
    # Extract alpha
    alpha = orig.split()[3]
    
    # Create a solid black background
    # This prevents the transparent pixels (which might be white/grey) from bleeding into the bezel during upscale
    solid_black = Image.new('RGBA', orig.size, (0, 0, 0, 255))
    
    # Composite the original over black
    # Now the entire image is opaque, and the screen hole is purely black.
    # The bezel is also black, so the transition is perfectly seamless.
    rgb_filled = Image.alpha_composite(solid_black, orig).convert('RGB')
    
    # Upscale the RGB channels to 4K (4096x2376)
    scale = 4
    new_size = (w * scale, h * scale)
    rgb_4k = rgb_filled.resize(new_size, resample=Image.LANCZOS)
    
    # Upscale the alpha channel
    # To prevent ringing, we threshold the original alpha to be perfectly sharp
    sharp_alpha = alpha.point(lambda p: 255 if p > 128 else 0)
    
    # Upscale the sharp alpha using Nearest Neighbor (preserves the sharp hard edge)
    alpha_4k = sharp_alpha.resize(new_size, resample=Image.NEAREST)
    
    # Now we have a jagged (aliased) 4K alpha mask. 
    # To make it perfectly smooth and anti-aliased, we apply a precise Gaussian blur.
    # A blur radius of 1.5 to 2.0 creates a beautiful soft anti-aliased edge at 4K.
    smooth_alpha = alpha_4k.filter(ImageFilter.GaussianBlur(1.8))
    
    # Combine the perfect RGB image with the perfect smooth Alpha mask
    rgb_4k.putalpha(smooth_alpha)
    
    # Save the flawless 4K mockup
    rgb_4k.save('public/mockups/macbook_8k.png')
    print("Flawless 4K mockup generated.")

process()
