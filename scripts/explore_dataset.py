import os
import matplotlib.pyplot as plt
from PIL import Image


# path to the dataset folder - change this if needed
DATASET_PATH = "data/kvasir-v2"


# loop through each class folder and count images
class_counts = {}

for class_name in os.listdir(DATASET_PATH):
    class_path = os.path.join(DATASET_PATH, class_name)

    # skip if it's not a folder
    if not os.path.isdir(class_path):
        continue

    count = 0
    for filename in os.listdir(class_path):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
            count += 1

    class_counts[class_name] = count

print("=" * 40)
print("Dataset Class Summary")
print("=" * 40)

# print the table header
print(f"{'Class Name':<30} {'Count':>6}")
print("-" * 40)

for class_name in class_counts:
    print(f"{class_name:<30} {class_counts[class_name]:>6}")

print("=" * 40)

# calculate basic stats
total_images = 0
for c in class_counts:
    total_images += class_counts[c]

counts_list = list(class_counts.values())
names_list = list(class_counts.keys())

min_count = min(counts_list)
max_count = max(counts_list)
mean_count = total_images / len(counts_list)

# find which class has min and max
min_class = ""
max_class = ""
for name in class_counts:
    if class_counts[name] == min_count:
        min_class = name
    if class_counts[name] == max_count:
        max_class = name

print(f"\nTotal images     : {total_images}")
print(f"Number of classes: {len(class_counts)}")
print(f"Min class        : {min_class} ({min_count} images)")
print(f"Max class        : {max_class} ({max_count} images)")
print(f"Mean per class   : {mean_count:.1f}")
print()

# create a bar chart
print("Creating bar chart...")

plt.figure(figsize=(12, 6))
plt.bar(names_list, counts_list, color="steelblue")
plt.xlabel("Class")
plt.ylabel("Number of Images")
plt.title("Kvasir Dataset - Images per Class")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# save the chart
output_path = "class_counts.png"
plt.savefig(output_path)
print(f"Chart saved to {output_path}")

plt.show()
