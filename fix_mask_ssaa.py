from PIL import Image, ImageDraw

def process():
    print("Generating 16K super-sampled mask...")
    
    # 4x the 4K size = 16384 x 9504
    scale = 4
    w_4k = 4096
    h_4k = 2376
    w_16k = w_4k * scale
    h_16k = h_4k * scale
    
    # Create 16K mask image (black = transparent)
    mask_16k = Image.new("L", (w_16k, h_16k), 0)
    draw = ImageDraw.Draw(mask_16k)
    
    # Base 4K coordinates:
    # Outer lid: left=392, right=3704, top=0, bottom=2376, radius=96
    # Inner hole: left=440, right=3652, top=48, bottom=2100, radius=36
    # Notch: left=1876, right=2220, top=48, bottom=108, radius=16
    
    def scale_box(b):
        return [b[0]*scale, b[1]*scale, b[2]*scale, b[3]*scale]
    
    # Draw outer lid (White = Opaque)
    outer_box = scale_box([392, 0, 3704, 2376])
    draw.rounded_rectangle(outer_box, radius=96*scale, fill=255)
    
    # Subtract inner screen hole (Black = Transparent)
    inner_box = scale_box([440, 48, 3652, 2100])
    draw.rounded_rectangle(inner_box, radius=36*scale, fill=0)
    
    # Add back the notch (White = Opaque)
    # The notch drops down from y=48. The top part connects to the bezel.
    notch_box = scale_box([1876, 32, 2220, 108]) # Start higher to overlap
    draw.rounded_rectangle(notch_box, radius=16*scale, fill=255)
    
    print("Downsampling to 4K for perfect SSAA...")
    mask_4k = mask_16k.resize((w_4k, h_4k), resample=Image.LANCZOS)
    
    # Process RGB
    orig = Image.open('public/mockups/macbook_new.png').convert('RGBA')
    solid_black = Image.new('RGBA', orig.size, (0, 0, 0, 255))
    rgb_filled = Image.alpha_composite(solid_black, orig).convert('RGB')
    
    print("Upscaling RGB to 4K...")
    rgb_4k = rgb_filled.resize((w_4k, h_4k), resample=Image.LANCZOS)
    
    print("Applying perfect anti-aliased mask...")
    rgb_4k.putalpha(mask_4k)
    
    rgb_4k.save('public/mockups/macbook_8k.png')
    print("Flawless 4K mockup generated.")

process()
