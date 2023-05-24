import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

import dearpygui.dearpygui as dpg
from scripts.crop_photo import PhotoHandler
from arrows_to_img.arrows_to_img import ImageProcessor


dpg.create_context()

def callback(sender, app_data):
    print('OK was clicked.')
    print("Sender: ", sender)
    print("App Data: ", app_data)
    
    

    if sender == "file_dialog_id_crop":
        path_chousen_crop = app_data['file_path_name']
        dpg.set_value("path_crop", f"path chousen for crop: {path_chousen_crop}")
        PhotoHandler.process_files_in_folder(PhotoHandler, path_chousen_crop)

    if sender == "file_dialog_id_arrows":
        path_chousen_arrows = app_data['file_path_name']
        dpg.set_value("path_arrows", f"path chousen for arrows: {path_chousen_arrows}")
        processor = ImageProcessor(path_chousen_arrows, "with_arrows")
        processor.process_folder()


def cancel_callback(sender, app_data):
    print('Cancel was clicked.')
    print("Sender: ", sender)
    print("App Data: ", app_data)

dpg.add_file_dialog(
    directory_selector=True, show=False, callback=callback, tag="file_dialog_id_crop",
    cancel_callback=cancel_callback, width=700 ,height=400)

dpg.add_file_dialog(
    directory_selector=True, show=False, callback=callback, tag="file_dialog_id_arrows",
    cancel_callback=cancel_callback, width=700 ,height=400)


def visible_call(sender, app_data):
    print("I'm visible")

with dpg.window(width=500, height=300):
    dpg.add_button(label="Directory Selector crop", callback=lambda: dpg.show_item("file_dialog_id_crop"))
    dpg.add_text("path chousen for crop: ", tag="path_crop")
    dpg.add_button(label="Directory Selector arrows", callback=lambda: dpg.show_item("file_dialog_id_arrows"))
    dpg.add_text("path chousen for arrows: ", tag="path_arrows")
    


dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()