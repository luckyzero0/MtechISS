import pandas as pd
from ydata_profiling import ProfileReport


FOLDER_PATH = 'C:/Users/weiji/Documents/Full Data.csv'

DATA_PATH = 'C:/Users/weiji/Documents/Full Data.csv'
OUTPUT_PATH = 'C:/Users/weiji/Documents/EDA_first_overall.html'

df = pd.read_csv(DATA_PATH)
MEASURES = ['CP AA ASIS NIR','MET AA ASIS NIR',
'LYS AA ASIS NIR', 'KOH PS RED ASIS NIR', 'TIA A RED ASIS NIR', 'LYS REACTIVE LYS RATIO RED ASIS NIR']
INTERESTED_COLUMNS = ['Country','Country of processing','Customer', 'Delivery date',
                      'Description','Lab customer', 'Lab no','Supplier'] + MEASURES

MAPPER = ''

df.columns = [c.upper() for c in df.columns]

df_filtered = df[[c.upper() for c in INTERESTED_COLUMNS]]
for m in MEASURES:
    if df_filtered[m].dtype == 'float64':
        continue
    else:
        df_filtered[m] = df_filtered[m].str.extract('([0-9.]+)').fillna(-1).apply(pd.to_numeric)


profile = ProfileReport(df_filtered, title='EDA First Overall Draft')
profile.to_file(OUTPUT_PATH)