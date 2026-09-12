import numpy as np
from scipy import ndimage
from PIL import Image

orig = Image.open('public/mockups/macbook_new.png').convert('RGBA')
alpha = np.array(orig.split()[3])
mask = alpha > 127
dist_inside = ndimage.distance_transform_edt(mask)
dist_outside = ndimage.distance_transform_edt(~mask)
sdf = dist_inside - dist_outside
sdf_img = Image.fromarray(sdf.astype(np.float32), mode='F')
scale = 4
w, h = orig.size
sdf_4k = sdf_img.resize((w*scale, h*scale), resample=Image.BICUBIC)
sdf_4k_arr = np.array(sdf_4k)

print('SDF values near x=448, y=200:')
for x in range(440, 455):
    print(f'x={x}: {sdf_4k_arr[200, x]}')
