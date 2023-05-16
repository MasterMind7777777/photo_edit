import cv2 as cv
import numpy as np
import os

class PhotoHandler(object):
    def photo_cropper(self, path):
        print(path)
        im = cv.imread(path)
        im_resized = cv.resize(im, None, fx=0.5, fy=0.5)  # Resize the image to improve processing

        imgray = cv.cvtColor(im_resized, cv.COLOR_BGR2GRAY)
        imgray = cv.medianBlur(imgray, 5)  # Apply median blur to reduce noise

        # Increase the block size and decrease the constant value for adaptive thresholding
        block_size = 21
        constant = 6
        thresh = cv.adaptiveThreshold(imgray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, block_size, constant)

        # Find top, bottom, left, and right pixels that are not background
        rows, cols = np.nonzero(thresh)
        top_scaled = np.min(rows)
        bottom_scaled = np.max(rows)
        left_scaled = np.min(cols)
        right_scaled = np.max(cols)

        margin_percentage = 0.02  # 2% margin

        if top_scaled < bottom_scaled and left_scaled < right_scaled:
            margin_x = int(margin_percentage * (right_scaled - left_scaled))
            margin_y = int(margin_percentage * (bottom_scaled - top_scaled))

            # Adjust the crop coordinates to avoid cropping the sides touching the image boundaries
            top_scaled -= margin_y
            bottom_scaled += margin_y
            left_scaled -= margin_x
            right_scaled += margin_x

            # Calculate crop coordinates for the original full-resolution image
            height, width = im.shape[:2]
            top = int(top_scaled * 2)  # Scaling factor is 0.5, so multiply by 2 to get the original scale
            bottom = int(bottom_scaled * 2)
            left = int(left_scaled * 2)
            right = int(right_scaled * 2)

            # Crop the image using the calculated coordinates
            if top >= 0 and bottom < height and left >= 0 and right < width:
                new_img = im[top:bottom, left:right]
            else:
                new_img = im  # If the crop coordinates are outside the image boundaries, save the entire image
        else:
            new_img = im  # If no suitable object is found, save the entire image

        cv.imwrite(
            os.path.join("cropped", f"{os.path.splitext(os.path.basename(path))[0]}.png"),
            new_img,
        )

    def process_files_in_folder(self, folder_path=""):
        print(folder_path)
        for root, directories, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                self.photo_cropper(self, file_path)

# process_files_in_folder
# im = cv.imread('test_img.jpg')
# assert im is not None, "file could not be read, check with os.path.exists()"
# photo_croper(im)

# ph = PhotoHandler

# PhotoHandler.process_files_in_folder(ph, folder_path = "C:\photo_test")