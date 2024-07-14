import tkinter
from pathlib import Path
from typing import Callable

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog

from collections import namedtuple
from main_util import start_side_button, start_up

def browseFiles():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("Text files",
                                                      "*.txt*"),
                                                     ("all files",
                                                      "*.*")))
    input_location_demand.set(value=filename)

def create_add_new_gui_screen(func_canvas):
    global input_location_demand, input_location_supply
    input_location_demand = tkinter.StringVar(func_canvas)

    label_box = tkinter.Label(func_canvas,
                      text = "New Data File",
                      fg = "black")

    func_canvas.create_window((1, 50), window=label_box, anchor='w')

    text_box = Entry(func_canvas, textvariable=input_location_demand, width=80)
    text_box.config(state='disabled')

    func_canvas.create_window((100, 50), height=30, window=text_box, anchor='w')

    button_explore = Button(func_canvas,
                            text = "Browse",
                            command = browseFiles)

    func_canvas.create_window((650, 50), window=button_explore, anchor='w')

    add_new = Button(func_canvas,
                     text = "Start Uploading",
                     command = lambda : print(f"Add New file: {input_location_demand.get()}"))

    func_canvas.create_window((720, 50), window=add_new, anchor='w')
    
    input_location_supply = tkinter.StringVar(func_canvas)

    label_box = tkinter.Label(func_canvas,
                      text = "New Supply File",
                      fg = "black")

    func_canvas.create_window((1, 100), window=label_box, anchor='w')

    text_box = Entry(func_canvas, textvariable=input_location_supply, width=80)
    text_box.config(state='disabled')

    func_canvas.create_window((100, 100), height=30, window=text_box, anchor='w')

    button_explore = Button(func_canvas,
                            text = "Browse",
                            command = browseFiles)

    func_canvas.create_window((650, 100), window=button_explore, anchor='w')

    add_new = Button(func_canvas,
                     text = "Start Uploading",
                     command = lambda : print(f"Add New file: {input_location_supply.get()}"))

    func_canvas.create_window((720, 100), window=add_new, anchor='w')


if __name__ == "__main__":
    global window, canvas, func_canvas
    window, canvas, func_canvas, info = start_up()
    side_buttons = start_side_button(window)
    create_add_new_gui_screen(func_canvas)
    window.mainloop()