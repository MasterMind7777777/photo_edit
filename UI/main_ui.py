import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

import dearpygui.dearpygui as dpg
from scripts.crop_photo import PhotoHandler


dpg.create_context()

def callback(sender, app_data):
    print('OK was clicked.')
    print("Sender: ", sender)
    print("App Data: ", app_data)
    path_chousen = app_data['file_path_name']
    dpg.set_value("path", f"path chousen: {path_chousen}")
    PhotoHandler.process_files_in_folder(PhotoHandler, path_chousen)


def cancel_callback(sender, app_data):
    print('Cancel was clicked.')
    print("Sender: ", sender)
    print("App Data: ", app_data)

dpg.add_file_dialog(
    directory_selector=True, show=False, callback=callback, tag="file_dialog_id",
    cancel_callback=cancel_callback, width=700 ,height=400)


def visible_call(sender, app_data):
    print("I'm visible")

with dpg.window(width=500, height=300):
    dpg.add_button(label="Directory Selector", callback=lambda: dpg.show_item("file_dialog_id"))
    dpg.add_text("path chosen: ", tag="path")
    


dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()