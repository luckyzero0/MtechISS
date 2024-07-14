import pandas as pd
from collections import defaultdict, namedtuple

DB_FILE = "C:/Users/USER/PycharmProjects/MtechISS/Final Capstone/GUI/build/assets/DB/DB File.xlsx"
DB_CONFIG = 'C:/Users/USER/PycharmProjects/MtechISS/Final Capstone/GUI/build/assets/DB/Department Short Codes.xlsx'

def refresh_database():
    global main_stats_month
    main_stats_month = pd.read_excel(DB_FILE, sheet_name='Month_Stats')
    return main_stats_month

def refresh_config():
    global department_config
    department_config = pd.read_excel(DB_CONFIG, sheet_name='Department_config')
    return department_config

def long_department_to_code(long_s:str):

    if long_s.upper() == 'ALL':
        return 'ALL'
    mapper = department_config[['Department Short Code','Department Long Code']].drop_duplicates()
    return mapper[mapper['Department Long Code'] == long_s]['Department Short Code'].iloc[0]

def code_to_long_department(code:str):

    if code.upper() == 'ALL':
        return 'ALL'
    mapper = department_config[['Department Short Code','Department Long Code']].drop_duplicates()
    return mapper[mapper['Department Short Code'] == code]['Department Long Code'].iloc[0]



def month2idx(months="Jul"):
    MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return MONTHS.index(months) + 1
def get_all_months_data(year:int=2024, month:int=1, department='ALL'):
    department_data = main_stats_month[main_stats_month.Department==department]
    filtered = department_data[department_data.Months.str.contains(str(year))]
    MonthData = namedtuple(typename='MonthData', field_names=['month_txt', 'per_txt', 'rec_colour'])
    MONTH_DATA = {'Year': str(year)}
    MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    for i in range(1,13):
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
        MONTH_DATA[MONTHS[i-1]] = MonthData(MONTHS[i-1], f'{percentage}%', color)

    filtered_months = department_data[department_data.Months == f"{str(year)}-{str(month).zfill(2)}"]
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
        statistics = {f'{MONTHS[month-1]} WTA': f'{filtered_months.Per_WTA}%',
                  f'{MONTHS[month-1]} Demand': f'{filtered_months.Demand}',
                  f'{MONTHS[month-1]} Supply': f'{filtered_months.Supply}',
                  f'{MONTHS[month-1]} Predicted WTA': '30%',
                  f'{MONTHS[month-1]} Total Expected': f'{filtered_months.Expected}',
                  f'{MONTHS[month-1]} Supply Adjustment': '130'
                  }


    return MONTH_DATA, statistics


def get_stats(year, month, department):
    stats = defaultdict(lambda: "No Stats")
    return stats

if __name__ == "__main__":
    pass