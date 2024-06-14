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

""" Data Selection: delete duplicates from the dataset """
data = DataProcessor().drop_duplicates(data)

""" Data Selection: delete irrelevant columns from the dataset """
data = DataProcessor().drop_columns(data, ["NCSC inschaling","Versie", "Schadeomschrijving", "Mogelijke oplossingen"])

""" Data Selection: delete rows where NCSC ID does not occure more than once """
data = data.loc[data.duplicated(subset=['NCSC ID'], keep=False)]
data = data.reset_index(drop=True)

""" Data Selection: change column Uitgiftedatum from object to datetime type """
data = DataProcessor().object_to_datetime(data, 'Uitgiftedatum')

""" Data Selection: check for outliers and missing values of Uitgiftedatum through a lineplot """
data_plot = data
data_plot.set_index('Uitgiftedatum', inplace=True)
grouped = data_plot.groupby(data_plot.index.year).size()
count_data = pd.DataFrame({'year': grouped.index, 'count': grouped.values})
count_data.plot(kind='line', x='year', y='count')
plt.title('Line plot of the Instances per Year')
plt.xlabel('Year')
plt.ylabel('Count')
plt.savefig('lineplot_Uitgiftedatum.png')
plt.show()

data = data.reset_index()

""" Data Cleaning: change column types """
DataAnalyzer().check_column_types(data)
# DataAnalyzer().print_selected_cell(data, 1, "NCSC ID")
DataProcessor().string_to_list(data, ['CVE-ID', "Toepassingen", "Versies", "Platformen"])
# print(data['CVE-ID'].apply(type))

""" Save intermediate dataset """
DataLoaderSaver().save_dataset(data, security_dataset, "processed")