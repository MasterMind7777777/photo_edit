import os
import cv2

def sort_images_in_folders(folder_path):
    image_files = []
    # Retrieve all image files in the folder
    for root, directories, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            if any(file_path.endswith(extension) for extension in ['.jpg', '.jpeg', '.png']):
                image_files.append(file_path)

    # Create a dictionary to store the grouped images
    image_groups = {}

    # Initialize SIFT feature extractor
    sift = cv2.SIFT_create()

    # Iterate over each image and compare with others
    for i in range(len(image_files)):
        image_a = cv2.imread(image_files[i])
        if image_a is None:
            continue

        # Extract keypoints and descriptors from image_a
        keypoints_a, descriptors_a = sift.detectAndCompute(image_a, None)

        # Compare with other images
        for j in range(i + 1, len(image_files)):
            image_b = cv2.imread(image_files[j])
            if image_b is None:
                continue

            # Extract keypoints and descriptors from image_b
            keypoints_b, descriptors_b = sift.detectAndCompute(image_b, None)

            # Initialize feature matcher
            matcher = cv2.BFMatcher()

            # Match keypoints
            matches = matcher.knnMatch(descriptors_a, descriptors_b, k=2)

            # Apply ratio test to filter good matches
            good_matches = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good_matches.append(m)

            # Group images if enough good matches are found
            min_match_count = 10
            if len(good_matches) >= min_match_count:
                if image_files[i] not in image_groups:
                    image_groups[image_files[i]] = [image_files[i]]
                image_groups[image_files[i]].append(image_files[j])

    return image_groups


folder_path = r'C:\projects\photo_edit\test_folder'  # Replace with the actual folder path
image_groups = sort_images_in_folders(folder_path)

# Print the sorted image groups
for representative_image, group_images in image_groups.items():
    print(f"Group: {representative_image}")
    print(f"Images: {group_images}")
    print()