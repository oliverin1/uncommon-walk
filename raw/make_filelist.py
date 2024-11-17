import os

file_pairs = []

for img in os.listdir('raw_dataset/jpeg_patches/'):
    filename = img.split('.jpg')[0]
    jpg_file = f'jpg_patches/{img}'
    npy_file = f'npy_patches/{filename}.npy'
    assert os.path.isfile(f'raw_dataset/{npy_file}')

    file_pairs.append(f'{jpg_file},{npy_file}')

filelist_str = "\n".join(file_pairs)
with open(f'raw_dataset/filelist.txt', "w") as f:
    f.write(filelist_str)
