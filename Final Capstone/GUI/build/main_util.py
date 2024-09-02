import logging
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from typing import Callable
import tkinter

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = Path(r".\assets\img")

SECONDARY_COLOR = "#030C5D"
BACKGROUND_COLOR = "#edfff6"
BTN_COLOR = '#007d3e'

DEPARTMENT = ['Gastroenterology','Orthopaedic Surgery', 'Otolaryngology']

DEFAULT_LABEL_FONT = dict(fg="black",
                          font=("Arial", 9, 'bold'),
                          bg=BACKGROUND_COLOR)


def relative_to_assets(path: str):
    return str(Path(ASSETS_PATH, path))


def create_button(window, file_asset: str, positions: dict, command: Callable) -> tkinter.Button:
    img = PhotoImage(file=relative_to_assets(file_asset))

    button = Button(window, image=img, borderwidth=0, highlightthickness=0, command=command, relief='flat', fg='green', bg='white')
    try:
        window.create_window((positions['x'], positions['y']), window=button)
    except AttributeError:
        button.place(**positions)
    return img, button


def start_up():
    from controller_db import refresh_department_config, refresh_database, refresh_configuration
    refresh_configuration()
    refresh_department_config()
    refresh_database()
    window = Tk()
    window.title("ApptInsight")
    window.geometry("1186x724")
    window.configure(bg="#FFFFFF")

    window.iconbitmap("./assets/img/image_1.ico")

    global canvas
    global func_canvas
    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=724,
        width=1186,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)
    func_canvas = Canvas(
        window,
        bg=BACKGROUND_COLOR,
        height=724,
        width=1186,
        bd=0,
        highlightthickness=0,
        relief='ridge'
    )
    func_canvas.place(x=300, y=100)

    appImage = PhotoImage(
        file=relative_to_assets("image_1.png"))
    mainapp_btn = Button(window, image=appImage, borderwidth=0, highlightthickness=0, bg="#ffffff", fg="#ffffff",
                         command=lambda: nav_main_gui(), relief='flat')
    mainapp_btn.place(x=20.0, y=20.0)
    # appimage_logo = canvas.create_image(
    #     49.0,
    #     44.0,
    #     image=appImage
    # )

    canvas.create_rectangle(
        0.0,
        88.0,
        1186.0,
        98,
        fill=BTN_COLOR,
        outline="")

    canvas.create_text(
        90.0,
        22.0,
        anchor="nw",
        text="ApptInsight",
        fill="#000000",
        font=("Inter Bold", 36 * -1)
    )

    canvas.create_rectangle(
        294,
        92,
        300,
        724,
        fill=BTN_COLOR,
        outline="")

    def get_pos(*args):
        print(args)

    func_canvas.bind("<Button-3>", get_pos)
    return window, canvas, func_canvas, (appImage, mainapp_btn)

    canvas.create_text(
        1000.0,
        34.0,
        anchor="nw",
        text="Last updated: 23 June 2024\nModel Updated Date: 23 April 2024",
        fill="#000000",
        font=("OpenSansItalic Regular", 9 * -1)
    )


def nav_add_new():
    clear_canvas_func()
    from add_new_gui import create_add_new_gui_screen
    create_add_new_gui_screen(func_canvas)


def nav_model_management():
    clear_canvas_func()
    from model_management_gui import create_model_management_screen
    create_model_management_screen(func_canvas)

def nav_configuration():
    clear_canvas_func()
    from model_management_gui import create_model_management_screen
    from configuration_gui import create_configuration_screen
    create_configuration_screen(func_canvas)


def nav_main_gui():
    clear_canvas_func()
    from main_gui import create_main_screen
    create_main_screen(func_canvas, startup=True)


def start_side_button(window):
    SIDE_TOOL_CONFIG = {
        'add_new_button': {
            'file_asset': 'add_new_button.png',
            'positions': dict(x=15.0, y=110.0),
            'command': lambda: nav_add_new()
        },
        # 'edit_button': {
        #     'file_asset': 'edit_existing_button.png',
        #     'positions': dict(x=15.0, y=190.0),
        #     'command': lambda: print("Edit Existing Clicked")
        # },

        # 'model_button': {
        #     'file_asset': 'model_management_button.png',
        #     'positions': dict(x=15.0, y=500.0, width=275.0),
        #     'command': lambda: nav_model_management()
        # },

        'config_button': {
            'file_asset': 'configuration_button.png',
            'positions': dict(x=15.0, y=580.0),
            'command': lambda: nav_configuration()
        },
    }
    SIDE_BUTTONS = {}
    for k, v in SIDE_TOOL_CONFIG.items():
        tmp = {}
        tmp['button'], tmp['img'] = create_button(window, **v)
        SIDE_BUTTONS[k] = tmp
    return SIDE_BUTTONS


def clear_canvas_func():
    func_canvas.delete('all')
    pass


class WidgetLogger(logging.Handler):
    def __init__(self, widget):
        logging.Handler.__init__(self)
        self.setLevel(logging.INFO)
        self.widget = widget
        self.widget.config(state='disabled')

    def emit(self, record):
        self.widget.config(state='normal')
        # Append message (record) to the widget
        self.widget.insert(tkinter.END, self.format(record) + '\n')
        self.widget.see(tkinter.END)  # Scroll to the bottom
        self.widget.config(state='disabled')


class ConsoleLogger:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.text_widget.config(state=tkinter.NORMAL)

    def write(self, message):
        self.text_widget.insert(tkinter.END, message)
        self.text_widget.see(tkinter.END)  # Scroll to the end of the text area

    def flush(self):
        pass  # No need to implement flush for this use case


class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, string):
        self.widget.configure(state="normal")
        self.widget.update()
        self.widget.insert("end", string, (self.tag,))
        self.widget.see(tkinter.END)
        self.widget.configure(state="disabled")
