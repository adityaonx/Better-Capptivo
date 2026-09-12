from PIL import Image, ImageFilter

def solidify(img):
    # Iterative dilation to smear edge colors into transparent areas
    rgb = img.convert('RGB')
    alpha = img.split()[3]
    
    # We will dilate multiple times
    for _ in range(5):
        # Create a blurred version of the current RGB
        blurred = rgb.filter(ImageFilter.BoxBlur(1))
        # Paste the blurred colors ONLY where the original alpha is 0
        # Wait, alpha is the original alpha, we want to expand the opaque area
        # A simpler way: just use a max filter (dilation) on the RGB channels!
        # But max filter brightens the image.
        pass

    return rgb

# Better solidify algorithm:
# For every transparent pixel, assign it the color of the nearest opaque pixel.
# In PIL, we can approximate this by repeatedly blending the image with a blurred version of itself, masked by the inverse of its current alpha.
