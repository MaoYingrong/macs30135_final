import os
import random
from itertools import combinations
from collections import defaultdict
import csv

# Store all pairs in a single list for final shuffling
all_pairs = []

# Process folders from c_0 to c_9
for i in range(10):
    folder_path = f"c_{i}"
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    files = [file_path for file_path in files if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    for file_path in files:
        # Check if the file is an image
        if not file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            print(f"Incorrect format for {file_path}")


    # Add folder name to file names to avoid duplicates
    files = [f"{folder_path}/{f}" for f in files]

    # Generate all unique combinations
    pairs = list(combinations(files, 2))

    # Randomly sample up to 500 pairs
    selected_pairs = random.sample(pairs, min(500, len(pairs)))

    all_pairs.extend(selected_pairs)

# Process folder c_-1 with class-based grouping
folder_path = "c_-1"
files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

# Add folder name to file names
files = [f"{folder_path}/{f}" for f in files]

# Step 1: Group files by class (prefix before '_')
class_groups = defaultdict(list)

for filename in files:
    class_prefix = filename.split('/')[-1].split('_')[0]  # Extract class prefix from filename
    class_groups[class_prefix].append(filename)

# Step 2: Generate all anchor-positive pairs across all classes in c_-1
for class_name, instances in class_groups.items():
    if len(instances) < 2:
        continue  # Skip classes with fewer than 2 instances

    # Generate all unique combinations within the class
    pairs = list(combinations(instances, 2))

    # Collect all pairs globally
    all_pairs.extend(pairs)

# Step 3: Shuffle the entire list of pairs globally
random.shuffle(all_pairs)

# Step 4: Separate into final anchor and positive lists
anchor, positive = zip(*all_pairs)

# Convert to lists
final_anchor_result = list(anchor)
final_positive_result = list(positive)

folder_path = "random_img_1000"
files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
files = [f"{folder_path}/{f}" for f in files]
extended_files = random.choices(files, k=len(final_anchor_result))  # Random sampling with replacement

output_file = "anchor_positive_pairs.csv"

# Write to CSV file
with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["anchor", "positive", "negative"])  # Header
    writer.writerows(zip(final_anchor_result, final_positive_result, extended_files))

print(f"Saved to {output_file}")