import pandas as pd
from collections import defaultdict

DB_FILE = "/assets/DB/DB File.xlsx"

main_stats_month = pd.read_excel(DB_FILE, sheet_name='Month_Stats')
def get_stats(year, month, department):
    stats = defaultdict(lambda: "No Stats")
    return stats


