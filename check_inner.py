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
w, h = img.size
alpha = img.split()[3]

print("--- Scanning for Inner left edge at y=200 ---")
for x in range(400, w):
    if alpha.getpixel((x, 200)) == 0:
        print(f"Inner left edge at x={x}")
        print_grid(img, x - 10, 200 - 5, 20, 10)
        break
