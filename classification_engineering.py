import pandas as pd

from DataLoaderSaver import DataLoaderSaver
from DataProcessor import DataProcessor
from ClassificationEngineering import ClassificationEngineering

""" Set dataset to run (NCSC/APT) """
security_dataset = "NCSC"

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
        df_row = df_row + 1

""" Add new columns with the changes to the new dataframe """
ClassificationEngineering().create_change_columns(df, "Kans")

ClassificationEngineering().print_overview(df,"Kans")

""" Delete irrelevant columns to clean up the new dataframe """
df = DataProcessor().drop_columns(df, ["Beschrijving old","Beschrijving new", "Kans old", "Kans new"])
print(df.shape)

""" Save intermediate dataset """
DataLoaderSaver().save_dataset(df, security_dataset, "classification")