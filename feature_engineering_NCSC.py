import pandas as pd

from DataLoaderSaver import DataLoaderSaver

""" Set dataset to run """
security_dataset = "NCSC"

""" Load initial dataset """
data = DataLoaderSaver().load_dataset(security_dataset, "processed")

""" Create new column with the number of updates per NCSC ID """
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

""" Save intermediate dataset """
DataLoaderSaver().save_dataset(data, security_dataset, "engineered")
