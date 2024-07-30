import pandas as pd
import matplotlib.pyplot as plt

from DataLoaderSaver import DataLoaderSaver
from DataAnalyzer import DataAnalyzer
from DataProcessor import DataProcessor
from ClassificationEngineering import ClassificationEngineering

""" Set dataset to run (NCSC/APT) """
security_dataset = "NCSC"
# security_dataset = "APT"

""" Load engineered dataset """
data = DataLoaderSaver().load_dataset(security_dataset, "engineered")

""" Create new dataframe """
data = data.sort_values(['NCSC ID', 'Update'])
data = data.reset_index(drop=True)

columns = ['NCSC ID', 'CVE-ID', 'Beschrijving old', 'Beschrijving new', 'Kans old', 'Kans new']
df = pd.DataFrame(columns=columns)
df_row = 0

for row in range(len(data)-1):
    if data.loc[row,'NCSC ID'] == data.loc[row + 1, 'NCSC ID']:
        df.loc[df_row, 'NCSC ID'] = data.loc[row,"NCSC ID"]
        df.loc[df_row, 'CVE-ID'] = data.loc[row, "CVE-ID"]
        df.loc[df_row, 'Beschrijving old'] = data.loc[row,"Beschrijving"]
        df.loc[df_row, 'Beschrijving new'] = data.loc[row + 1,"Beschrijving"]
        df.loc[df_row, 'Kans old'] = data.loc[row,"Kans"]
        df.loc[df_row, 'Kans new'] = data.loc[row + 1,"Kans"]
        # df.loc[df_row, 'Schade old'] = data.loc[row,"Schade"]
        # df.loc[df_row, 'Schade new'] = data.loc[row + 1,"Schade"]
        df_row = df_row + 1

""" Add new columns with the changes to the new dataframe """
ClassificationEngineering().create_change_columns(df, "Kans")
# ClassificationEngineering().create_change_columns(df, "Schade")

ClassificationEngineering().print_overview(df,"Kans")
# ClassificationEngineering().print_overview(df,"Schade")

# """ Add one new classification column about the changes of the Kans related to the Beschrijving """
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

""" Code to check elements of the new dataframe """
# print(df)
# DataAnalyzer().print_column_names(df)
# DataAnalyzer().print_selected_value(df, "NCSC ID", 'NCSC-2023-0023')
# DataAnalyzer().print_selected_cell(df, 14241, "Beschrijving old")
# DataAnalyzer().print_selected_cell(df, 14241, "Beschrijving new")

""" Delete irrelevant columns to clean up the new dataframe """
df = DataProcessor().drop_columns(df, ["Beschrijving old","Beschrijving new", "Kans old", "Kans new"])
print(df.shape)

""" Save intermediate dataset """
DataLoaderSaver().save_dataset(df, security_dataset, "classification")