import os
from PIL import Image


# path to the dataset - same as explore_dataset.py
DATASET_PATH = "data/kvasir-v2"


print("Checking images in dataset...")
print()

widths = []
heights = []
file_sizes = []
corrupt_images = []
total_count = 0

# go through every class folder
for class_name in os.listdir(DATASET_PATH):
    class_path = os.path.join(DATASET_PATH, class_name)

    if not os.path.isdir(class_path):
        continue

    for filename in os.listdir(class_path):
        if not (filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg")):
            continue

        img_path = os.path.join(class_path, filename)
        total_count += 1

        # get file size in bytes
        size_bytes = os.path.getsize(img_path)
        file_sizes.append(size_bytes)

        # try to open image - if it fails it's probably corrupt
        try:
            img = Image.open(img_path)
            img.verify()  # this checks if the file is broken
            w, h = img.size
            widths.append(w)
            heights.append(h)
        except Exception as e:
            print(f"  [CORRUPT] {img_path} -> {e}")
            corrupt_images.append(img_path)

print(f"Total images scanned: {total_count}")
print()

# calculate resolution stats
if len(widths) > 0:
    min_w = min(widths)
    max_w = max(widths)
    avg_w = sum(widths) / len(widths)

    min_h = min(heights)
    max_h = max(heights)
    avg_h = sum(heights) / len(heights)

    print("Resolution Stats:")
    print(f"  Min : {min_w} x {min_h}")
    print(f"  Max : {max_w} x {max_h}")
    print(f"  Avg : {avg_w:.0f} x {avg_h:.0f}")
    print()

# total dataset size
total_bytes = sum(file_sizes)
total_mb = total_bytes / (1024 * 1024)
print(f"Total dataset size: {total_mb:.2f} MB")
print()

# report corrupt images
if len(corrupt_images) == 0:
    print("No corrupt images found. All good!")
else:
    print(f"Found {len(corrupt_images)} corrupt image(s):")
    for path in corrupt_images:
        print(f"  - {path}")
