import tkinter
from datetime import datetime

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from main_util import *
from collections import namedtuple
from controller_db import month2idx, code_to_long_department, long_department_to_code, predict_upload, create_month_year
from add_new_gui import refresh_WTA

global window, canvas, func_canvas, STATE, DEPARTMENT

def get_month_data(*args):
    """
    To Get the clicked month Data

    :param args:
    :return: None
    """
    selected_month = func_canvas.gettags('current')[0].replace("_btm", "")
    selected_month_idx = month2idx(selected_month)
    STATE['month'] = selected_month_idx
    clear_canvas_func()
    create_main_screen(func_canvas, startup=False)


def refresh_wta_month(*args):
    """
    To Refresh the selected Month for the predicted and actual WTA calculation

    :param args:
    :return:
    """
    selected_month = func_canvas.gettags('current')[0].replace("_btm", "")
    selected_month_idx = month2idx(selected_month)
    selected_department = STATE['department']
    selected_year = STATE['year']
    combined_year_month = create_month_year(selected_year, selected_month_idx)
    refresh_WTA([{'months': combined_year_month, "department": selected_department}], category='actual')
    refresh_WTA([{'months': combined_year_month, "department": selected_department}], category='predicted')
    STATE['month'] = selected_month_idx

    clear_canvas_func()
    create_main_screen(func_canvas, startup=False)


def get_department(value: str):
    """
    To get the department selected from the drop down

    :param value: drop down value
    :return: None
    """
    from controller_db import long_department_to_code
    short_code_department = long_department_to_code(value)
    STATE['department'] = short_code_department

    clear_canvas_func()
    create_main_screen(func_canvas, startup=False)

    # print(f"Currently selected {value}, {short_code_department}")
    # print(f"Current State", STATE)


def create_month(x, y, month_txt, per_txt, rec_colour, SIZE_OF_WIDGET=(120, 110), outline='#000000', outline_width=1):
    """
    To get the month selected

    :param x: Left top position of X
    :param y: Left top position of Y
    :return: None
    """

    main_rec = func_canvas.create_rectangle(x, y, x + SIZE_OF_WIDGET[0], y + SIZE_OF_WIDGET[1], fill='#FFFFFF',
                                            width=outline_width, outline=outline, tags=f'{month_txt}_btm')

    func_canvas.tag_bind(f'{month_txt}_btm', "<Button-1>", get_month_data)
    func_canvas.tag_bind(f'{month_txt}_btm', "<Button-3>", refresh_wta_month)

    CENTER_X_OF_WIDGET = (x + SIZE_OF_WIDGET[0] / 2)
    func_canvas.create_text(CENTER_X_OF_WIDGET, y + 17, anchor="center", text=month_txt, fill="#000000",
                            font=("ArimoRoman Bold", 20 * -1))
    PAD = 20
    func_canvas.create_rectangle(x + PAD, y + 40, x + SIZE_OF_WIDGET[0] - PAD, y + 40 + 20, fill=rec_colour,
                                 outline='black', tags=f'{month_txt}_btm')
    func_canvas.tag_bind(f'{month_txt}_btm', "<Button-1>", get_month_data)
    func_canvas.tag_bind(f'{month_txt}_btm', "<Button-3>", refresh_wta_month)

    func_canvas.create_text(CENTER_X_OF_WIDGET, y + 40 + 20 + 17, anchor='center', text=per_txt, fill='#000000',
                            font=("ArimoRoman Bold", 20 * -1))

def nav_year(func):
    if func=='increase':
        STATE['year'] = STATE['year'] + 1
    elif func=='decrease':
        STATE['year'] = STATE['year'] - 1
    clear_canvas_func()
    create_main_screen(func_canvas, startup=False)

# Rectangle for dropdown
def create_month_grid(func_canvas, month_data, selected=0):
    """
    To create a grid of the months in the GUI

    Parameters:
    :param func_canvas: Tkinter window (Main)
    :param month_data: Months data to be populated by functions
    :param selected: selected Months

    :return:
    """
    # START_GRID = (360, 220)
    START_GRID = (60, 120)

    SIZE_OF_WIDGET = (120, 110)
    X_PAD = 10
    Y_PAD = 20
    CUR_XY = {'x': START_GRID[0], 'y': START_GRID[1]}

    # Rectangle for monthly Grid
    func_canvas.create_rectangle(
        29.0,
        81.0,
        865.0,
        551.0,
        fill="#FFFFFF",
        outline="black")

    YEAR_LOCATION = (413, 85)

    func_canvas.create_text(
        YEAR_LOCATION[0],
        YEAR_LOCATION[1],
        anchor="nw",
        text=month_data['Year'],
        fill="#000000",
        font=("ArimoRoman Bold", 20 * -1)
    )
    button4, img = create_button(func_canvas, file_asset='right_button.png', positions=dict(x=480, y=95),
                                 command=lambda: nav_year('increase'))
    button5, img = create_button(func_canvas, file_asset='left_button.png', positions=dict(x=380, y=95),
                                 command=lambda: nav_year('decrease'))
    global YEAR_BTN
    YEAR_BTN = [(button4, img), (button5, img)]

    # button6, img = create_button(func_canvas, file_asset='')

    for idx, (k, v) in enumerate(month_data.items()):
        if k == 'Year':
            continue
        else:
            if idx == selected:

                outline = config.BTN_COLOR
                width = '3'
            else:
                outline = '#000000'
                width = 1
            CUR_XY.update(v._asdict())
            create_month(outline_width=width, outline=outline, SIZE_OF_WIDGET=SIZE_OF_WIDGET, **(CUR_XY))
            if k != 'Jun':
                CUR_XY = {'x': CUR_XY['x'] + X_PAD + SIZE_OF_WIDGET[0], 'y': CUR_XY['y']}
            else:
                CUR_XY = {'x': START_GRID[0], 'y': START_GRID[1] + Y_PAD + SIZE_OF_WIDGET[1]}


def create_statistic(func_canvas, statistic):
    """
    Create the statistic

    :param func_canvas: Tkinter window
    :param statistic:
    :return:
    """
    TITLE = (382, 380)
    func_canvas.create_text(
        *TITLE,
        anchor="nw",
        text="Statistics",
        fill="#000000",
        font=("ArimoRoman Bold", 20 * -1)
    )
    START_POS = (200, 420)
    CUR_POS = START_POS

    Y_PAD = 40
    X_PAD = 400
    SPACE = 150

    # Rectangle for statistic
    func_canvas.create_rectangle(
        60.0,
        372.0,
        830.0,
        535.0,
        fill="#FFFFFF",
        outline="black")
    statistic_d = {}
    for idx, (k, v) in enumerate(statistic.items()):
        key_var = tkinter.StringVar(func_canvas, value=k + ":")

        t_box = tkinter.Label(master=func_canvas, textvariable=key_var, bg=config.BACKGROUND_COLOR,
                              font=("ArimoRoman Bold", 20 * -1,), justify='right')
        func_canvas.create_window((CUR_POS[0], CUR_POS[1]), window=t_box)

        v_var = tkinter.StringVar(func_canvas, value=v)
        v_box = tkinter.Label(master=func_canvas, textvariable=v_var, bg=config.BACKGROUND_COLOR,
                              font=("ArimoRoman Bold", 20 * -1),
                              justify='left', )

        func_canvas.create_window((CUR_POS[0] + SPACE, CUR_POS[1]), window=v_box)

        CUR_POS = (CUR_POS[0], CUR_POS[1] + Y_PAD)
        if idx == 2:
            CUR_POS = (START_POS[0] + X_PAD, START_POS[1])
        statistic_d[idx] = {'k': key_var, 'v': v_var}
    return statistic, statistic_d


def create_main_screen(func_canvas, startup=False):
    """

    Parameters:
    :param func_canvas: Tkinter Window
    :param startup: Startup
    :return:
    """
    global statistics, MONTH_DATA, statistics_d, STATE

    from controller_db import get_all_months_data, refresh_database
    from config import refresh_configuration, DEPARTMENT, refresh_department_config
    refresh_configuration()
    refresh_database()
    refresh_department_config()
    if startup == True:
        STATE = dict(year=datetime.now().year,
                     month=datetime.now().month,
                     department=long_department_to_code(DEPARTMENT[0])
                     )
    selected_year = STATE.get('year')
    selected_month = STATE.get('month')
    selected_department = STATE.get('department')
    MONTH_DATA, statistics = get_all_months_data(selected_year, selected_month, selected_department)
    REC = [30, 20, 865, 65]
    func_canvas.create_rectangle(
        *REC,
        fill=config.SECONDARY_COLOR,
        outline="black")
    cur_select_department = tkinter.StringVar()
    selected_department_long = code_to_long_department(selected_department)
    cur_select_department.set(selected_department_long)
    dropdown = tkinter.OptionMenu(func_canvas, cur_select_department, *DEPARTMENT, command=get_department)
    dropdown.configure(bg=("%s" % config.SECONDARY_COLOR), fg='#FFFFFF', font=("OpenSansRoman Bold", 20 * -1), borderwidth=0,
                       highlightthickness=0)
    func_canvas.create_window((450, 40), window=dropdown)
    create_month_grid(func_canvas, MONTH_DATA, selected=selected_month)
    statistics, statistics_d = create_statistic(func_canvas, statistics)


if __name__ == "__main__":
    global window, canvas, func_canvas
    window, canvas, func_canvas, info = start_up()
    side_buttons = start_side_button(window)
    create_main_screen(func_canvas, startup=True)
    window.resizable(False, False)
    window.mainloop()
