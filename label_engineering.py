import pandas as pd
import matplotlib.pyplot as plt

from DataLoaderSaver import DataLoaderSaver
from DataAnalyzer import DataAnalyzer
from DataProcessor import DataProcessor

""" Load engineered dataset """
data = DataLoaderSaver().load_dataset("engineered", "$")

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

print("Total:", df['No change'].sum() + df['Unjustified change'].sum() + df['Unimportant change'].sum() + df['Justified+important change'].sum())
print(len(df))

""" Add one new classification column about the changes related to the Beschrijving """
df['Change'] = ""

for row in range(len(df)):
    if df.loc[row,'Beschrijving old'] == df.loc[row, 'Beschrijving new'] and df.loc[row,'Kans old'] == df.loc[row, 'Kans new']:
        df.loc[row,'Change'] = "No change" #0
    elif (df.loc[row,'Beschrijving old'] == df.loc[row, 'Beschrijving new']) and (df.loc[row,'Kans old'] != df.loc[row, 'Kans new']):
        df.loc[row,'Change'] = "Unjustified" #1
    elif (df.loc[row,'Beschrijving old'] != df.loc[row, 'Beschrijving new']) and (df.loc[row,'Kans old'] == df.loc[row, 'Kans new']):
        df.loc[row,'Change'] = "Unimportant" #2
    elif (df.loc[row,'Beschrijving old'] != df.loc[row, 'Beschrijving new']) and (df.loc[row,'Kans old'] != df.loc[row, 'Kans new']):
        df.loc[row,'Change'] = "Justified & important" #3

DataAnalyzer().print_selected_columns(df, ["No change","Change"])

""" Save intermediate dataset """
DataLoaderSaver().save_dataset(df,"labelled", "$")