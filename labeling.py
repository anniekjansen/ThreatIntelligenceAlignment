import pandas as pd
import matplotlib.pyplot as plt

from DataLoaderSaver import DataLoaderSaver
from DataAnalyzer import DataAnalyzer
from DataProcessor import DataProcessor

""" Load processed dataset """
data = DataLoaderSaver().load_dataset("processed")

""" Create dataframe which includes multiple updates (Advisory IDs) for the same NCSC ID """
# DataAnalyzer().check_uniques_columns(data, ['Advisory ID', 'NCSC ID'])

""" Delete rows where NCSC ID does not occure more often """
data = data.loc[data.duplicated(subset=['NCSC ID'], keep=False)]
data = data.reset_index(drop=True)
# DataAnalyzer().print_selected_value(data, "NCSC ID", 'NCSC-2023-0023')
# DataAnalyzer().check_uniques_columns(data, ['Advisory ID', 'NCSC ID'])

""" Create dataframe of necessary columns, including new column with the number of updates per NCSC ID """
data = data[['Advisory ID','NCSC ID', 'Uitgiftedatum','Beschrijving', 'Kans']]
data = data.sort_values(by='Uitgiftedatum')
data = data.reset_index(drop=True)

data['Update'] = pd.Series(dtype='int')
NCSC_ids = []

for row in range(len(data)):
    if data.loc[row,'NCSC ID'] not in NCSC_ids:
        NCSC_ids.append(data.loc[row,'NCSC ID'])
        data.loc[row,'Update'] = 1
    elif data.loc[row,'NCSC ID'] in NCSC_ids:
        count = NCSC_ids.count(data.loc[row,'NCSC ID'])
        data.loc[row,'Update'] = count + 1
        NCSC_ids.append(data.loc[row,'NCSC ID'])

# print(data.head(5))
# print(len(NCSC_ids))
# DataAnalyzer().check_uniques_columns(data, ['NCSC ID','Update'])
# DataAnalyzer().print_histogram(data, "Update")

""" Create new dataframe """
data = data.sort_values(['NCSC ID', 'Update'])
data = data.reset_index(drop=True)

# DataAnalyzer().print_selected_value(data, "NCSC ID", 'NCSC-2022-0610')

df = data[['NCSC ID']]
df_row = 0

for row in range(len(data)-1):
    if data.loc[row,'NCSC ID'] == data.loc[row + 1, 'NCSC ID']:
        df.loc[df_row, 'Beschrijving old'] = data.loc[row,"Beschrijving"]
        df.loc[df_row, 'Beschrijving new'] = data.loc[row + 1,"Beschrijving"]
        df.loc[df_row, 'Kans old'] = data.loc[row,"Kans"]
        df.loc[df_row, 'Kans new'] = data.loc[row + 1,"Kans"]
        df_row = df_row + 1

""" Add new columns with the changes to the new dataframe """
df['No change'] = 0
df['Unjustified change'] = 0
df['Unimportant change'] = 0
df['Justified+important change'] = 0

for row in range(len(df)):
    if df.loc[row,'Beschrijving old'] == df.loc[row, 'Beschrijving new'] and df.loc[row,'Kans old'] == df.loc[row, 'Kans new']:
        df.loc[row,'No change'] = 1
    elif (df.loc[row,'Beschrijving old'] == df.loc[row, 'Beschrijving new']) and (df.loc[row,'Kans old'] != df.loc[row, 'Kans new']):
        df.loc[row,'Unjustified change'] = 1
    elif (df.loc[row,'Beschrijving old'] != df.loc[row, 'Beschrijving new']) and (df.loc[row,'Kans old'] == df.loc[row, 'Kans new']):
        df.loc[row,'Unimportant change'] = 1
    elif (df.loc[row,'Beschrijving old'] != df.loc[row, 'Beschrijving new']) and (df.loc[row,'Kans old'] != df.loc[row, 'Kans new']):
        df.loc[row,'Justified+important change'] = 1

print("No change:", df['No change'].sum())
print("Unjustified change:", df['Unjustified change'].sum())
print("Unimportant change:", df['Unimportant change'].sum())
print("Justified+important change:", df['Justified+important change'].sum())

DataLoaderSaver().save_dataset(df,"labelled", "$")
