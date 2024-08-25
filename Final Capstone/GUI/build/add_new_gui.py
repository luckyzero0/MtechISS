import datetime
import logging
import sys
import tkinter
from ast import literal_eval
from pathlib import Path
from typing import Callable

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog, scrolledtext

from collections import namedtuple

from dateutil.relativedelta import relativedelta

from main_util import start_side_button, start_up, WidgetLogger, ConsoleLogger, TextRedirector, BACKGROUND_COLOR, \
    DEFAULT_LABEL_FONT
from controller_db import get_supply, upload_demand, upload_supply, get_WTA, update_data, DB_FILE, refresh_database, \
    _predict_upload, predict_upload


def browseFilesDemand():
    filename = filedialog.askopenfilenames(initialdir="./",
                                           title="Select a File",

                                           filetypes=(("Excel files",
                                                       "*.xlsx*"),
                                                      ("all files",
                                                       "*.*")))
    input_location_demand.set(value=filename)


def browseFilesSupply():
    filename = filedialog.askopenfilenames(initialdir="./",
                                           title="Select a File",

                                           filetypes=(("Excel files",
                                                       "*.xlsx*"),
                                                      ("all files",
                                                       "*.*")))
    input_location_supply.set(value=filename)


def get_next_n_months(start_month, n=3):
    start_date = datetime.datetime.strptime(start_month, "%Y-%m")
    months_list = [(start_date + relativedelta(months=i)).strftime("%Y-%m") for i in range(n)]
    return months_list


def get_WTA_data(category, month, department):
    main_stats_month = refresh_database()
    months = get_next_n_months(start_month=month)

    filtered = main_stats_month.query(f"Months in {tuple(months)} and Department == '{department}'")
    print(filtered)
    if category == 'actual':
        demand = filtered.Demand.values
    elif category == "predicted":
        demand = filtered.Predicted_Demand.values
    slots_booked = filtered.Slot_booked.values
    supply = filtered.Supply
    return demand, supply, slots_booked


def refresh_WTA(new_ds, category='actual'):
    for x in new_ds:
        demand, supply, slots_booked = get_WTA_data(category, month=x.get('months'), department=x.get('department'))
        if len(demand) < 3:
            continue
        wta = get_WTA(demand, supply, slots_booked)
        print(f"WTA Calculated: {wta}")
        temp = {
            'months': x.get('months'),
            'department': x.get('department')
        }
        if category == 'actual':
            temp['actual_wta'] = wta
        elif category == 'predict':
            temp['predict_wta'] = wta
        update_data(DB_FILE, temp)



def start_uploading_demand():
    if input_location_demand.get():
        print("Starting_upload_demand")
        new_ds = upload_demand(literal_eval(input_location_demand.get()))
    else:
        return
    print("Upload_demand Ended")
    print("Starting Prediction")
    predict_upload(new_ds)
    print("Starting_WTA_calculation")
    refresh_WTA(new_ds, category='predicted')
    input_location_demand.set("")
    print("Completed uploaded")


def start_uploading_supply():
    print("Starting_upload_supply")
    new_ds = upload_supply(literal_eval(input_location_supply.get()))
    print("Upload_supply Ended")
    print("Starting_WTA_calculation")
    refresh_WTA(new_ds, category='predicted')
    input_location_supply.set("")
    print("Completed uploaded")


def create_add_new_gui_screen(func_canvas):
    global input_location_demand, input_location_supply
    input_location_demand = tkinter.StringVar(func_canvas)

    label_box = tkinter.Label(func_canvas,
                              text="New Data File",
                              **DEFAULT_LABEL_FONT
                              )

    func_canvas.create_window((95, 50), window=label_box, anchor='e')

    text_box = Entry(func_canvas, textvariable=input_location_demand, width=80)
    text_box.config(state='disabled')

    func_canvas.create_window((100, 50), height=30, window=text_box, anchor='w')

    button_explore = Button(func_canvas,
                            text="Browse",
                            command=browseFilesDemand)

    func_canvas.create_window((650, 50), window=button_explore, anchor='center')

    add_new = Button(func_canvas,
                     text="Start Uploading",
                     command=lambda: start_uploading_demand())

    func_canvas.create_window((720, 50), window=add_new, anchor='w')

    input_location_supply = tkinter.StringVar(func_canvas)

    label_box = tkinter.Label(func_canvas,
                              text="New Supply File",
                              **DEFAULT_LABEL_FONT)

    func_canvas.create_window((95, 100), window=label_box, anchor='e')

    text_box = Entry(func_canvas, textvariable=input_location_supply, width=80)
    text_box.config(state='disabled')

    func_canvas.create_window((100, 100), height=30, window=text_box, anchor='w')

    button_explore = Button(func_canvas,
                            text="Browse",
                            command=browseFilesSupply)

    func_canvas.create_window((650, 100), window=button_explore, anchor='center')

    add_new = Button(func_canvas,
                     text="Start Uploading",
                     command=lambda: start_uploading_supply())

    func_canvas.create_window((720, 100), window=add_new, anchor='w')

    scroll_logs = scrolledtext.ScrolledText(state='disabled')
    scroll_logs.configure(font='TkFixedFront')

    sys.stdout = TextRedirector(scroll_logs, "stdout")
    sys.stderr = TextRedirector(scroll_logs, "stderr")

    func_canvas.create_window((400, 380), window=scroll_logs)


if __name__ == "__main__":
    global window, canvas, func_canvas
    window, canvas, func_canvas, info = start_up()
    side_buttons = start_side_button(window)
    create_add_new_gui_screen(func_canvas)
    window.mainloop()
