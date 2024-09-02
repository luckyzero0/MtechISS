import tkinter
from pathlib import Path
from typing import Callable

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog

from collections import namedtuple

import pandas as pd

from main_util import start_side_button, start_up, DEFAULT_LABEL_FONT
from controller_db import refresh_configuration, CONFIGURATION_EXCEL, append_config



def create_configuration_screen(func_canvas):
    refresh_configuration()
    global input_location_model, configuration_df
    configuration_df = pd.read_excel(CONFIGURATION_EXCEL)

    POS_X = 5
    POS_Y = 20
    DIFF = 50
    for idx, r in configuration_df.iterrows():
        label_box = tkinter.Label(func_canvas,
                                  text=r['Config Key'],
                                  **DEFAULT_LABEL_FONT)
        func_canvas.create_window((POS_X, POS_Y), window=label_box, anchor='w')
        var = tkinter.StringVar()
        var.set(r['Config Value'])
        label_text = Entry(func_canvas, textvariable=var, width=120)
        func_canvas.create_window((POS_X, POS_Y+20), window=label_text, anchor='w', height=20)
        POS_Y += DIFF

    add_new = Button(func_canvas,
                            text = "Save Settings",
                            command = lambda : append_config())


    func_canvas.create_window((763, 500), window=add_new, anchor='w')

if __name__ == "__main__":
    global window, canvas, func_canvas
    window, canvas, func_canvas, info = start_up()
    side_buttons = start_side_button(window)
    create_configuration_screen(func_canvas)
    window.mainloop()