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

print("--- Top-Left Outer Corner ---")
alpha = img.split()[3]
w, h = img.size
found = False
for y in range(0, 100):
    for x in range(0, 500):
        if alpha.getpixel((x, y)) > 0:
            print(f"Top-left starts around x={x}, y={y}")
            print_grid(img, x - 2, y - 2, 20, 10)
            found = True
            break
    if found: break
