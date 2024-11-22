import dearpygui.dearpygui as dpg
import dearpygui_grid as dpg_grid
import math
import os
import datetime

window_W = 1000
window_H = 800
n = int(window_W / math.gcd(window_W, window_H))

text = "hello world"

def create_file(sender, app_data, user_data):
    print("created file")

def transfer_file(sender, app_data, user_data):
    print("transferred file")

def read_file(filepath):
    with open(filepath) as f:
        return f.read()

def get_metadata(filepath):
    file_stat = os.stat(filepath)

    metadata = {
        "File name" : os.path.basename(filepath),
        "File size" : file_stat.st_size,
        "Created time" : datetime.datetime.fromtimestamp(file_stat.st_ctime),
        "Modified time" : datetime.datetime.fromtimestamp(file_stat.st_mtime),
        "Accessed time" : datetime.datetime.fromtimestamp(file_stat.st_atime),
        "Is directory" : os.path.isdir(filepath)
    }

    return metadata

def open_file(sender, app_data, user_data):
    dpg.show_item("open_file")

def show_file(sender, app_data, user_data):
    filepath = [file for file in app_data['selections']]
    filename = filepath[0]
    filepath = app_data['selections'][filename]
    contents = read_file(filepath)
    metadata = get_metadata(filepath)
    with dpg.window(label=filename, pos=[0,0], width=window_W/2, height=window_H):
        dpg.add_text(contents)
    with dpg.window(label="Metadata", pos=[window_W/2, 0], width=window_W/2, height=window_H):
        for k,v in metadata.items():
            dpg.add_text(str(k) + ":" + str(v))

dpg.create_context()
with dpg.font_registry():
    default_font = dpg.add_font("GeistMono-VariableFont_wght.ttf", 10)
    big_font = dpg.add_font("GeistMono-VariableFont_wght.ttf", 26)
dpg.create_viewport(title="Quriosity - QID", width=window_W, height=window_H)

with dpg.file_dialog(directory_selector=False, show=False, callback=show_file, tag="open_file", width=800, height=600):
    dpg.add_file_extension(".*")


with dpg.window(    tag="primary_window",
                    pos=[0,0],
                    width=dpg.get_viewport_client_width()-1,
                    height=dpg.get_viewport_client_height()-1,
                    no_title_bar=True,
                    no_move=True,
                    no_scrollbar=True) as window:

    grid = dpg_grid.Grid(3,3, window)

    grid.push(dpg.add_button(label="Open file", parent=window, callback=open_file), 1,0)
    grid.push(dpg.add_button(label="Create file", parent=window, callback=create_file), 1,1)
    grid.push(dpg.add_button(label="Transfer file", parent=window, callback=transfer_file), 1,2)

    dpg.bind_font(big_font)

    with dpg.item_handler_registry() as window_hr:
        dpg.add_item_visible_handler(callback=grid)
    dpg.bind_item_handler_registry(window, window_hr)


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("primary_window", True)
dpg.start_dearpygui()
dpg.destroy_context()