import cv2
import numpy as np
import os
import pandas as pd

class ImageProcessor:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder

    def process_folder(self):
        # Get the list of files in the input folder
        file_list = os.listdir(self.input_folder)
        print(file_list)

        # Process each file in the folder
        for file_name in file_list:
            
            # Construct the input and output paths
            input_path = os.path.join(self.input_folder, file_name)
            output_path = os.path.join(self.output_folder)
            print(file_name)
            print(output_path + file_name)
            # Process the image file
            self.draw_matrix_arrows(input_path, output_path + "/" + file_name)
            self.add_numbers_from_excel(output_path + "/" + file_name, file_name)

    def draw_matrix_arrows(self, image_path, output_path):
        # Load the image
        image = cv2.imread(image_path)

        # Convert the image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Get the dimensions of the image
        height, width = gray_image.shape
        area = height * width

        # Calculate the square size based on the image dimensions
        square_size = int(np.sqrt(area) / 120 * (area / (area * 0.2)))

        # Calculate the number of squares in each dimension
        num_squares_height = height // square_size
        num_squares_width = width // square_size

        # Calculate the center point of the first column and last row
        first_column_center = square_size // 2
        last_row_center = (num_squares_height - 1) * square_size

        # Set the size of the arrow tip
        arrow_tip_size = int(1 * square_size) + int(area / 500000)

        # Create an empty canvas to draw the arrows and squares
        canvas = np.copy(image)

        # Draw the arrow in the middle of the first column pointing up
        cv2.arrowedLine(
            canvas,
            (square_size, last_row_center),
            (square_size, first_column_center),
            (0, 0, 0),
            thickness=2,
            tipLength=arrow_tip_size / height,
        )

        # Draw the arrow in the middle of the last row pointing right
        cv2.arrowedLine(
            canvas,
            (square_size, last_row_center),
            (width - square_size, last_row_center),
            (0, 0, 0),
            thickness=2,
            tipLength=arrow_tip_size / width,
        )

        # Draw the matrix representation
        for i in range(num_squares_height):
            for j in range(num_squares_width):
                x = j * square_size
                y = i * square_size
                cv2.rectangle(
                    canvas, (x, y), (x + square_size, y + square_size), (0, 0, 0), thickness=1
                )

        # Save the image with arrows and squares
        if output_path != "":
            cv2.imwrite(output_path, canvas)

        # Return the calculated values
        return square_size, first_column_center, arrow_tip_size


    def add_numbers_from_excel(self, image_path, file_name):
        # Load the Excel file
        excel_file = pd.read_excel("test.xlsx")
        print(excel_file)

        # Find the corresponding number for the given file name
        number = excel_file.loc[excel_file['Filename'] == file_name, 'Number'].values

        if len(number) > 0:
            number = int(number[0])

            # Load the image
            image = cv2.imread(image_path)

            # Get the dimensions of the image
            height, width, _ = image.shape

            # Set the font properties
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_thickness = 2

            # Determine the position to place the number
            text = str(number)
            text_width, text_height = cv2.getTextSize(text, font, font_scale, font_thickness)[0]

            # Calculate the position next to the arrow tip
            square_size, first_column_center, arrow_tip_size = self.draw_matrix_arrows(image_path, "")

            arrow_tip_x = square_size + int(0.5 * square_size)
            arrow_tip_y = first_column_center
            text_x = arrow_tip_x + arrow_tip_size
            text_y = arrow_tip_y + arrow_tip_size + text_height

            # Add the number to the image
            cv2.putText(image, text, (text_x, text_y), font, font_scale, (0, 0, 0), font_thickness)

            # Save the updated image
            cv2.imwrite(image_path, image)



# Example usage
input_folder = "arrows_to_img/input"
output_folder = "arrows_to_img/output"
processor = ImageProcessor(input_folder, output_folder)
processor.process_folder()