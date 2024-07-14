import tkinter
from pathlib import Path
from typing import Callable

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog

from collections import namedtuple
from main_util import start_side_button, start_up

def browseFiles():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("Pickle files",
                                                      "*.pkl*"),
                                                     ("all files",
                                                      "*.*")))
    input_location_model.set(value=filename)

def create_model_management_screen(func_canvas):
    global input_location_model
    input_location_model = tkinter.StringVar(func_canvas)

    label_box = tkinter.Label(func_canvas,
                      text = "Current Model",
                      fg = "black")

    func_canvas.create_window((1, 55), window=label_box, anchor='w')

    text_box = Entry(func_canvas, textvariable=input_location_model,  width=90)
    text_box.config(state='disabled')

    func_canvas.create_window((90, 55), height=30, window=text_box, anchor='w')

    button_explore = Button(func_canvas,
                            text = "Browse Files",
                            command = browseFiles)


    func_canvas.create_window((680, 55), window=button_explore, anchor='w')


    add_new = Button(func_canvas,
                            text = "Save Settings",
                            command = lambda : print(f"Add New file: {input_location_model.get()}"))


    func_canvas.create_window((763, 133), window=add_new, anchor='w')

    func_canvas.create_rectangle(
        0.0,
        200.0,
        1186.0,
        205,
        fill="#009C54",
        outline="")

    global output_location_model, output_model_settings
    output_location_model = tkinter.StringVar(func_canvas)
    output_model_settings = tkinter.StringVar(func_canvas)

    label_box = tkinter.Label(func_canvas,
                      text = "Output Model Path",
                      fg = "black")

    func_canvas.create_window((1, 220), window=label_box, anchor='w')


    text_box = Entry(func_canvas, textvariable=output_location_model,  width=80)
    text_box.config(state='disabled')

    func_canvas.create_window((150, 220), height=30, window=text_box, anchor='w')


    button_explore = Button(func_canvas,
                            text = "Browse Files",
                            command = browseFiles)

    func_canvas.create_window((680, 220), window=button_explore, anchor='w')


    label_box = tkinter.Label(func_canvas,
                      text = "Output Model Settings",
                      fg = "black")

    func_canvas.create_window((1, 280), window=label_box, anchor='w')

    text_box = Entry(func_canvas, textvariable=output_model_settings,  width=80)
    text_box.config(state='disabled')

    func_canvas.create_window((150, 280), window=text_box, height=30, anchor='w')

    button_explore = Button(func_canvas,
                            text = "Browse Files",
                            command = browseFiles)


    func_canvas.create_window((680, 280), window=button_explore, anchor='w')

    add_new = Button(func_canvas,
                            text = "Start Training",
                            command = lambda : print(f"Add New file: {output_model_settings.get()}"))

    func_canvas.create_window((763, 350), window=add_new, anchor='w')

    model_training_output_box = Text(func_canvas, height=13, width=105, bg='white', borderwidth=3)

    func_canvas.create_window((1, 500), window=model_training_output_box, anchor='w')

if __name__ == "__main__":
    global window, canvas, func_canvas
    window, canvas, func_canvas, info = start_up()
    side_buttons = start_side_button(window)
    create_model_management_screen()
    window.mainloop()