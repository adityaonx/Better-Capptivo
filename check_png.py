from PIL import Image

def print_grid(img, start_x, start_y, w, h):
    alpha = img.split()[3]
    for y in range(start_y, start_y + h):
        row = ""
        for x in range(start_x, start_x + w):
            val = alpha.getpixel((x, y))
            if val == 0: row += "  "
            elif val < 64: row += ". "
            elif val < 128: row += "- "
            elif val < 192: row += "+ "
            elif val < 255: row += "* "
            else: row += "# "
        print(row)

img = Image.open('public/mockups/macbook_8k.png')

# We need to find where the top-left outer corner actually is in the 4K image!
# Let's search for the first non-zero alpha pixel in the top left.
w, h = img.size
alpha = img.split()[3]
found = False
for y in range(0, h):
    for x in range(0, w):
        if alpha.getpixel((x, y)) > 0:
            print(f"Top-left outer corner starts around x={x}, y={y}")
            print_grid(img, x - 5, y - 5, 30, 20)
            found = True
            break
    if found: break

print("\n--- Inner Hole Corner ---")
# Inner hole is around x=440, y=48. Let's find it.
# Scan right from x=300 at y=100
for x in range(300, w):
    if alpha.getpixel((x, 100)) == 0:
        print(f"Inner hole left edge at y=100 is around x={x}")
        print_grid(img, x - 10, 100 - 10, 30, 20)
        break

