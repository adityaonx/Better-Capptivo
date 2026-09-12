import cairosvg
from PIL import Image

def process():
    # 1. Generate perfect mathematical SVG mask
    # The mask needs to be white where the laptop is opaque, and black where it is transparent (the hole & outside).
    # We use a 4096 x 2376 canvas.
    # Outer box: left=440-12*4=392, right=3652+13*4=3704, top=0, bottom=2376
    # Outer radius: 24 * 4 = 96
    # Inner box: left=440, right=3652, top=48, bottom=2100
    # Inner radius: 10 * 4 = 40
    # Notch: left=469*4=1876, right=555*4=2220, top=48, bottom=27*4=108
    # Notch radius: 4 * 4 = 16
    
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 4096 2376" width="4096" height="2376">
      <defs>
        <!-- The main laptop body is white (opaque) -->
        <!-- The screen hole is black (transparent) -->
        <mask id="laptop-mask">
          <!-- Entire image is black (transparent) -->
          <rect x="0" y="0" width="4096" height="2376" fill="black" />
          
          <!-- Draw the laptop lid as white (opaque) -->
          <!-- We only need to round the top corners, bottom goes off-screen -->
          <path d="M 392 96 A 96 96 0 0 1 488 0 L 3608 0 A 96 96 0 0 1 3704 96 L 3704 2376 L 392 2376 Z" fill="white" />
          
          <!-- Subtract the screen hole (draw it black) -->
          <rect x="440" y="48" width="3212" height="2052" rx="40" fill="black" />
          
          <!-- Add back the notch (draw it white) -->
          <!-- The notch hangs from the top edge (y=48) down to y=108 -->
          <!-- We draw a rounded rect but the top part merges with the bezel -->
          <rect x="1876" y="20" width="344" height="88" rx="20" fill="white" />
        </mask>
      </defs>
      
      <!-- Render the mask to the visible canvas as greyscale -->
      <rect x="0" y="0" width="4096" height="2376" fill="black" />
      <path d="M 392 96 A 96 96 0 0 1 488 0 L 3608 0 A 96 96 0 0 1 3704 96 L 3704 2376 L 392 2376 Z" fill="white" />
      <rect x="440" y="48" width="3212" height="2052" rx="36" fill="black" />
      <path d="M 1876 48 L 2220 48 L 2220 92 A 16 16 0 0 1 2204 108 L 1892 108 A 16 16 0 0 1 1876 92 Z" fill="white" />
    </svg>"""

    # Write SVG to file
    with open('mask.svg', 'w') as f:
        f.write(svg)

    # Convert SVG to PNG using cairosvg
    cairosvg.svg2png(url='mask.svg', write_to='mask.png')
    print("Rendered perfect SVG mask to mask.png")

    # Load the mask
    mask_img = Image.open('mask.png').convert('L')
    
    # Process RGB
    orig = Image.open('public/mockups/macbook_new.png').convert('RGBA')
    w, h = orig.size
    
    solid_black = Image.new('RGBA', orig.size, (0, 0, 0, 255))
    rgb_filled = Image.alpha_composite(solid_black, orig).convert('RGB')
    
    scale = 4
    new_size = (w * scale, h * scale)
    # Upscale RGB using high-quality Lanczos
    rgb_4k = rgb_filled.resize(new_size, resample=Image.LANCZOS)
    
    # Apply the mathematically perfect SVG mask!
    rgb_4k.putalpha(mask_img)
    
    rgb_4k.save('public/mockups/macbook_8k.png')
    print("Flawless 4K mockup with true SVG anti-aliasing generated.")

process()
