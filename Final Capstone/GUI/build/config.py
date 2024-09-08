from collections import defaultdict
from pathlib import Path

import pandas as pd

OUTPUT_PATH = Path(__file__).parent
DB_FILE = "./assets/DB/DB File.xlsx"
DB_CONFIG = './assets/DB/Department Short Codes.xlsx'
CONFIGURATION_EXCEL = './assets/DB/Configuration.xlsx'
DEFAULT_SEARCH_FOLDER = './'
ASSETS_PATH = Path(r".\assets\img")

SECONDARY_COLOR = "#030C5D"
BACKGROUND_COLOR = "#edfff6"
BTN_COLOR = '#007d3e'



DEFAULT_LABEL_FONT = dict(fg="black",
                          font=("Arial", 9, 'bold'),
                          bg=BACKGROUND_COLOR)

def refresh_configuration():
    configuration_df = pd.read_excel(CONFIGURATION_EXCEL)
    CONFIGURATION = zip(configuration_df['Config Key'], configuration_df['Config Value'])
    globals().update(CONFIGURATION)
    return CONFIGURATION

def refresh_department_config():
    global department_config
    department_config = pd.read_excel(DB_CONFIG, sheet_name='Department_config')
    return department_config

CONFIGURATION = refresh_configuration()
department_config = refresh_department_config()
DEPARTMENT = department_config['Department Long Code'].unique()
SHORT_DEPARTMENT =department_config['Department Short Code'].unique()
