import pandas as pd
import matplotlib.pyplot as plt

from DataLoaderSaver import DataLoaderSaver
from DataAnalyzer import DataAnalyzer
from DataProcessor import DataProcessor
from DataEngineering import DataEngineering

""" Load engineered dataset """
data = DataLoaderSaver().load_dataset("engineered", "$")

""" Create new dataframe """
data = data.sort_values(['NCSC ID', 'Update']) ## Use version
data = data.reset_index(drop=True)

df = data[['NCSC ID']]
df_row = 0

for row in range(len(data)-1):
    if data.loc[row,'NCSC ID'] == data.loc[row + 1, 'NCSC ID']:
        df.loc[df_row, 'Beschrijving old'] = data.loc[row,"Beschrijving"]
        df.loc[df_row, 'Beschrijving new'] = data.loc[row + 1,"Beschrijving"]
        df.loc[df_row, 'Kans old'] = data.loc[row,"Kans"]
        df.loc[df_row, 'Kans new'] = data.loc[row + 1,"Kans"]
        df.loc[df_row, 'Schade old'] = data.loc[row,"Schade"]
        df.loc[df_row, 'Schade new'] = data.loc[row + 1,"Schade"]
        df_row = df_row + 1

""" Add new columns with the changes to the new dataframe """
DataEngineering().create_change_columns(df, "Kans")
DataEngineering().create_change_columns(df, "Schade")

DataEngineering().print_overview(df,"Kans")
DataEngineering().print_overview(df,"Schade")

# OR

# """ Add one new classification column about the changes related to the Beschrijving """
# df['Change'] = ""

# for row in range(len(df)):
#     if df.loc[row,'Beschrijving old'] == df.loc[row, 'Beschrijving new'] and df.loc[row,'Kans old'] == df.loc[row, 'Kans new']:
#         df.loc[row,'Change'] = "No change" #0
#     elif (df.loc[row,'Beschrijving old'] == df.loc[row, 'Beschrijving new']) and (df.loc[row,'Kans old'] != df.loc[row, 'Kans new']):
#         df.loc[row,'Change'] = "Unjustified" #1
#     elif (df.loc[row,'Beschrijving old'] != df.loc[row, 'Beschrijving new']) and (df.loc[row,'Kans old'] == df.loc[row, 'Kans new']):
#         df.loc[row,'Change'] = "Unimportant" #2
#     elif (df.loc[row,'Beschrijving old'] != df.loc[row, 'Beschrijving new']) and (df.loc[row,'Kans old'] != df.loc[row, 'Kans new']):
#         df.loc[row,'Change'] = "Justified & important" #3

""" Save intermediate dataset """
DataLoaderSaver().save_dataset(df,"labelled", "$")