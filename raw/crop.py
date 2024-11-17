import numpy as np
import rawpy
import cv2
import imageio.v3 as iio
import os

dim = 768

for img in os.listdir('raw_dataset/arw/'):
    if not img.endswith('ARW'):
        continue
    print(img)

    with rawpy.imread(f'raw_dataset/arw/{img}') as raw:
        raw_image = raw.raw_image
        rgb_image = raw.postprocess(output_bps=16)
    h, w, _ = rgb_image.shape
    horizontal = False if h > w else True

    # top, left, bottom, right
    if horizontal:
        tx1, ty1, tx2, ty2 = 0,     0,     w//2,     w//2
        yx1, yy1, yx2, yy2 = w//2,   0,     w,       w//2
        gx1, gy1, gx2, gy2 = 0,     h-w//2, w//2,     h
        hx1, hy1, hx2, hy2 = w//2,   h-w//2, w,       h
    else:
        tx1, ty1, tx2, ty2 = 0,     0,     h//2,     h//2
        yx1, yy1, yx2, yy2 = w-h//2,0,     w,       h//2
        gx1, gy1, gx2, gy2 = 0,     h//2,  h//2,     h
        hx1, hy1, hx2, hy2 = w-h//2,h//2,  w,       h

    patch_y = cv2.resize(rgb_image[yy1:yy2, yx1:yx2], dsize=(dim, dim), interpolation=cv2.INTER_AREA)
    patch_t = cv2.resize(rgb_image[ty1:ty2, tx1:tx2], dsize=(dim, dim), interpolation=cv2.INTER_AREA)
    patch_g = cv2.resize(rgb_image[gy1:gy2, gx1:gx2], dsize=(dim, dim), interpolation=cv2.INTER_AREA)
    patch_h = cv2.resize(rgb_image[hy1:hy2, hx1:hx2], dsize=(dim, dim), interpolation=cv2.INTER_AREA)
    assert(patch_t.shape == patch_y.shape == patch_g.shape == patch_h.shape == (dim, dim, 3))

    # horizontal flip for augmentation
    if horizontal:
        patch_g = patch_g[:, ::-1]
        patch_h = patch_h[:, ::-1]
    else:
        patch_y = patch_y[:, ::-1]
        patch_h = patch_h[:, ::-1]

    patch_t_jpg = (patch_t / 256).astype('uint8')
    patch_y_jpg = (patch_y / 256).astype('uint8')
    patch_g_jpg = (patch_g / 256).astype('uint8')
    patch_h_jpg = (patch_h / 256).astype('uint8')

    # save raw patches as npy
    np.save(f'raw_dataset/npy_patches/{img}_t.npy', patch_t)
    np.save(f'raw_dataset/npy_patches/{img}_y.npy', patch_y)
    np.save(f'raw_dataset/npy_patches/{img}_g.npy', patch_g)
    np.save(f'raw_dataset/npy_patches/{img}_h.npy', patch_h)
    
    # save tiff patches
    #iio.imwrite(f'raw_dataset/patches/{img}_t.tiff', patch_t)
    #iio.imwrite(f'raw_dataset/patches/{img}_y.tiff', patch_y)
    #iio.imwrite(f'raw_dataset/patches/{img}_g.tiff', patch_g)
    #iio.imwrite(f'raw_dataset/patches/{img}_h.tiff', patch_h)

    # save jpeg patches
    #iio.imwrite(f'raw_dataset/jpeg_patches/{img}_t.jpg', patch_t_jpg)
    #iio.imwrite(f'raw_dataset/jpeg_patches/{img}_y.jpg', patch_y_jpg)
    #iio.imwrite(f'raw_dataset/jpeg_patches/{img}_g.jpg', patch_g_jpg)
    #iio.imwrite(f'raw_dataset/jpeg_patches/{img}_h.jpg', patch_h_jpg)

    #break
