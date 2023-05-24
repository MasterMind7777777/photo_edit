def process_folder(input_folder, output_folder):
    # Get the list of files in the input folder
    file_list = os.listdir(input_folder)

    # Process each file in the folder
    for file_name in file_list:
        # Construct the input and output paths
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name)

        # Process the image file
        draw_matrix_arrows(input_path, output_path)