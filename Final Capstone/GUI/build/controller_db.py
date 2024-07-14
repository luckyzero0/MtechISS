import pandas as pd
from collections import defaultdict, namedtuple

DB_FILE = "C:/Users/USER/PycharmProjects/MtechISS/Final Capstone/GUI/build/assets/DB/DB File.xlsx"


def refresh_database():
    global main_stats_month
    main_stats_month = pd.read_excel(DB_FILE, sheet_name='Month_Stats')
    return main_stats_month

def get_all_months_data(year=2024, month=1):
    filtered = main_stats_month[main_stats_month.Months.str.contains(str(year))]
    MonthData = namedtuple(typename='MonthData', field_names=['month_txt', 'per_txt', 'rec_colour'])
    MONTH_DATA = {'Year': str(year)}
    MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    for i in range(12):
        output = filtered.query(f"Months == '{year}-{str(i).zfill(2)}'")
        if len(output) == 0:
            percentage = 0
        else:
            percentage = output.iloc[0]['Per_WTA']

        THRESHOLD = [90,80,50]
        def get_colour(percentage):
            if percentage > THRESHOLD[0]:
                return 'red'
            elif percentage > THRESHOLD[1]:
                return 'orange'
            elif percentage > THRESHOLD[2]:
                return 'yellow'
            else:
                return 'green'
        color = get_colour(percentage)
        MONTH_DATA[MONTHS[i]] = MonthData(MONTHS[i], f'{percentage}%', color)
    month = month - 1
    filtered_months = main_stats_month[main_stats_month.Months == f"{str(year)}-{str(month).zfill(2)}"]
    if len(filtered_months) == 0:
        statistics = {f'{MONTHS[month]} WTA': '-',
                  f'{MONTHS[month]} Demand': '-',
                  f'{MONTHS[month]} Supply': '-',
                  f'{MONTHS[month]} Predicted WTA': '-',
                  f'{MONTHS[month]} Total Expected': '-',
                  f'{MONTHS[month]} Supply Adjustment': '-'
                  }

    else:
        filtered_months = filtered_months.iloc[0].fillna(0)
        statistics = {f'{MONTHS[month]} WTA': f'{filtered_months.Per_WTA}%',
                  f'{MONTHS[month]} Demand': f'{filtered_months.Demand}',
                  f'{MONTHS[month]} Supply': f'{filtered_months.Supply}',
                  f'{MONTHS[month]} Predicted WTA': '30%',
                  f'{MONTHS[month]} Total Expected': f'{filtered_months.Expected}',
                  f'{MONTHS[month]} Supply Adjustment': '130'
                  }


    return MONTH_DATA, statistics


def get_stats(year, month, department):
    stats = defaultdict(lambda: "No Stats")
    return stats

if __name__ == "__main__":
    pass