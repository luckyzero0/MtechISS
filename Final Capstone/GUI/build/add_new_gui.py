import datetime

import sys
import tkinter
from ast import literal_eval


from tkinter import  Entry, Button, filedialog, scrolledtext
import config
from config import refresh_configuration


from dateutil.relativedelta import relativedelta

from main_util import start_side_button, start_up, TextRedirector, set_notice
from controller_db import  upload_demand, upload_supply, get_WTA, update_data, refresh_database, predict_upload


def browseFilesDemand():
    initial_dir = config.DEFAULT_SEARCH_FOLDER
    filename = filedialog.askopenfilenames(initialdir=initial_dir,
                                           title="Select a File",

                                           filetypes=(("Excel files",
                                                       "*.xlsx*"),
                                                      ("all files",
                                                       "*.*")))
    input_location_demand.set(value=filename)


def browseFilesSupply():
    initial_dir = config.DEFAULT_SEARCH_FOLDER
    filename = filedialog.askopenfilenames(initialdir=initial_dir,
                                           title="Select a File",

                                           filetypes=(("Excel files",
                                                       "*.xlsx*"),
                                                      ("all files",
                                                       "*.*")))
    input_location_supply.set(value=filename)


def get_next_n_months(start_month, n=3):
    """
    Get a list of Nth month after start month, including itself
    :param start_month:
    :param n:
    :return:
    """
    start_date = datetime.datetime.strptime(start_month, "%Y-%m")
    if n < 0:
        months_list = [(start_date - relativedelta(months=i)).strftime("%Y-%m") for i in range(0, (n*-1)+1 )]
    else:
        months_list = [(start_date + relativedelta(months=i)).strftime("%Y-%m") for i in range(0, n+1)]
    return months_list


def get_WTA_data(category, month, department):
    main_stats_month = refresh_database()
    months = get_next_n_months(start_month=month, n=3)

    filtered = main_stats_month.query(f"Months in {tuple(months)} and Department == '{department}'").sort_values(
        'Months')

    if category == 'actual':
        demand = filtered.Demand.values
    elif category == "predicted":
        demand = filtered.Predicted_Demand.values
    else:
        raise "Incorrect Category in get_WTA_data function"
    slots_booked = filtered.Slot_booked.fillna(0).values
    supply = filtered.Supply.values
    return demand, supply, slots_booked


def refresh_WTA(new_ds, category='actual', full=True):
    def _refresh_WTA(month):
        demand, supply, slots_booked = get_WTA_data(category=category, month=month,
                                                    department=x.get('department'))
        if len(demand) < 3:
            return -1
        wta = get_WTA(demand, supply, slots_booked)
        print(f"{category} WTA Calculated: {wta}")
        temp = {
            'months': month,
            'department': x.get('department')
        }
        if category == 'actual':
            temp['actual_wta'] = wta
        elif category == 'predicted':
            temp['predicted_wta'] = wta
        else:
            print("Incorrect category")
        update_data(config.DB_FILE, temp)

    for x in new_ds:
        if full:
            _refresh_WTA(get_next_n_months(x.get('months'), -1)[-1])
            _refresh_WTA(get_next_n_months(x.get('months'), 1)[-1])
            _refresh_WTA(get_next_n_months(x.get('months'), 2)[-1])

        _refresh_WTA(x.get('months'))


def start_uploading_demand():
    if input_location_demand.get():
        set_notice("Starting_upload_demand")

        new_ds = upload_demand(literal_eval(input_location_demand.get()))
    else:
        return
    print("Upload_demand Ended")
    set_notice("Starting Prediction")

    predict_upload(new_ds)
    set_notice("Starting_WTA_calculation")
    refresh_WTA(new_ds, category='actual')
    refresh_WTA(new_ds, category='predicted')
    input_location_demand.set("")
    set_notice("""Completed upload""")



def start_uploading_supply():
    print("Starting_upload_supply")
    new_ds = upload_supply(literal_eval(input_location_supply.get()))
    print("Upload_supply Ended")
    print("Starting_WTA_calculation")
    refresh_WTA(new_ds, category='actual')
    refresh_WTA(new_ds, category='predicted')
    input_location_supply.set("")
    print("Completed uploaded")


def create_add_new_gui_screen(func_canvas):
    global input_location_demand, input_location_supply
    refresh_configuration()
    input_location_demand = tkinter.StringVar(func_canvas)

    label_box = tkinter.Label(func_canvas,
                              text="New Data File",
                              **config.DEFAULT_LABEL_FONT
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
                              **config.DEFAULT_LABEL_FONT)

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

    scroll_logs = scrolledtext.ScrolledText(state='disabled', height=20, width=70)
    scroll_logs.configure(font='TkFixedFront')

    sys.stdout = TextRedirector(scroll_logs, "stdout")
    sys.stderr = TextRedirector(scroll_logs, "stderr")

    func_canvas.create_window((45, 150), window=scroll_logs, anchor='nw')


if __name__ == "__main__":
    global window, canvas, func_canvas
    window, canvas, func_canvas, info = start_up()
    side_buttons = start_side_button(window)
    create_add_new_gui_screen(func_canvas)
    window.mainloop()
