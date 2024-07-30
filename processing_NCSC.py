import pandas as pd
import matplotlib.pyplot as plt
import ast

from DataLoaderSaver import DataLoaderSaver
from DataAnalyzer import DataAnalyzer
from DataProcessor import DataProcessor

""" Set dataset to run """
security_dataset = "NCSC"

""" Load initial dataset """
data = DataLoaderSaver().load_dataset(security_dataset, "initial")

""" Data Selection """

""" Delete duplicates from the dataset """
data = DataProcessor().drop_duplicates(data)

""" Delete irrelevant columns from the dataset """
data = DataProcessor().drop_columns(data, ["NCSC inschaling","Versie", "Schadeomschrijving", "Mogelijke oplossingen"])

""" Delete rows where NCSC ID does not occure more than once """
data = data.loc[data.duplicated(subset=['NCSC ID'], keep=False)]
data = data.reset_index(drop=True)

""" Change column Uitgiftedatum from object to datetime type """
data = DataProcessor().object_to_datetime(data, 'Uitgiftedatum')

""" Check for outliers and missing values of Uitgiftedatum through a lineplot """
data.set_index('Uitgiftedatum', inplace=True)
data.index = pd.to_datetime(data.index)

fig, ax = plt.subplots(figsize=(10, 6))
counts = data.resample('A').size().sort_index()
ax.plot(counts.index, counts.values, label='Uitgiftedatum')

ax.set_title('Count per Year')
ax.set_xlabel('Year')
ax.set_ylabel('Count')
ax.legend()
ax.grid(True)

# plt.savefig('lineplot_Uitgiftedatum.png')
plt.show()

data = data.reset_index()

""" Data Cleaning """

""" Change column types and clean input to None if applicable """
# DataAnalyzer().check_column_types(data)
data = DataProcessor().string_to_list(data, ['CVE-ID', "Toepassingen", "Versies", "Platformen"])
data = DataProcessor().values_to_None(data, ['CVE-ID', "Toepassingen", "Versies", "Platformen"])

""" Delete instances where CVE-ID is None """
print(data.isna().sum())
data = data.dropna(subset=["CVE-ID"])

""" Clean instances where CVE-ID contains CVE-IDs in a wrong format (spaces or punctuation) """
for index, row in data.iterrows():
    fixed_cve_ids = [DataProcessor().fix_cve_id(cve_id) for cve_id in row["CVE-ID"]]
    fixed_cve_ids = [cve_id for cve_id in [DataProcessor().valid_cve_id(cve_id) for cve_id in fixed_cve_ids] if cve_id is not None]
    data.at[index, "CVE-ID"] = fixed_cve_ids

""" Delete again instances where CVE-ID is None """
data = DataProcessor().values_to_None(data, ['CVE-ID'])
print(data.isna().sum())
data = data.dropna(subset=["CVE-ID"])

""" Save intermediate dataset """
DataLoaderSaver().save_dataset(data, security_dataset, "processed")