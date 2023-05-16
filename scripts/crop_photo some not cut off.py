import cv2 as cv
import numpy as np
import os

class PhotoHandler(object):

	def photo_croper(path):
		print(path)
		im = cv.imread(path)
		im = cv.resize(im, None, fx=0.5, fy=0.5)  # Resize the image to improve processing (adjust the scaling factor as needed)
		imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
		imgray = cv.medianBlur(imgray, 5)  # Apply median blur to reduce noise

		# Increase the block size and decrease the constant value for adaptive thresholding
		block_size = 21
		constant = 6
		thresh = cv.adaptiveThreshold(imgray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, block_size, constant)

		# Find top, bottom, left, and right pixels that are not background
		rows, cols = np.nonzero(thresh)
		top = np.min(rows)
		bottom = np.max(rows)
		left = np.min(cols)
		right = np.max(cols)

		margin_percentage = 0.02  # 2% margin

		if top < bottom and left < right:
			margin_x = int(margin_percentage * (right - left))
			margin_y = int(margin_percentage * (bottom - top))

			# Adjust the crop coordinates to avoid cropping the sides touching the image boundaries
			if top > margin_y:
				top -= margin_y
			if bottom + margin_y < im.shape[0]:
				bottom += margin_y
			if left > margin_x:
				left -= margin_x
			if right + margin_x < im.shape[1]:
				right += margin_x

			new_img = im[top:bottom, left:right]
			cv.imwrite(
				"cropped/"
				+ path.split("\\")[-1].replace(".JPG", "")
				+ ".png",
				new_img,
			)
		else:
			# If no suitable object is found, save the entire image
			cv.imwrite(
				"cropped/"
				+ path.split("\\")[-1].replace(".JPG", "")
				+ ".png",
				im,
			)

	def process_files_in_folder(self, folder_path=""):
		print(folder_path)
		for root, directories, filenames in os.walk(folder_path):
			for filename in filenames:
				file_path = os.path.join(root, filename)
				self.photo_croper(file_path)




# process_files_in_folder
# im = cv.imread('test_img.jpg')
# assert im is not None, "file could not be read, check with os.path.exists()"
# photo_croper(im)

# ph = PhotoHandler

# PhotoHandler.process_files_in_folder(ph, folder_path = "C:\photo_test")