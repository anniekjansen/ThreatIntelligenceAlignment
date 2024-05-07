import pandas as pd
import matplotlib.pyplot as plt

from DataLoaderSaver import DataLoaderSaver
from DataAnalyzer import DataAnalyzer
from DataProcessor import DataProcessor

""" Set dataset to run (NCSC/APT) """
security_dataset = "NCSC"
# security_dataset = "APT"

""" Load initial dataset """
data = DataLoaderSaver().load_dataset(security_dataset, "initial")

""" Delete duplicates from the dataset """
data = DataProcessor().drop_duplicates(data)

""" Delete irrelevant columns from the dataset """
data = DataProcessor().drop_columns(data, ["NCSC inschaling","Versies"])

""" Delete rows where NCSC ID does not occure more than once """
data = data.loc[data.duplicated(subset=['NCSC ID'], keep=False)]
data = data.reset_index(drop=True)

""" Change column Uitgiftedatum from object to datetime type """
data = DataProcessor().object_to_datetime(data)

""" Check for outliers and consistency of Advisory ID through a boxplot """
print(print(data.dtypes))
DataProcessor().create_boxplot(data, 'Advisory ID')
DataAnalyzer().check_uniques_columns(data, ['Advisory ID'])
print(data.shape)

""" Check for outliers and missing values of Uitgiftedatum through a lineplot """
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

""" Save intermediate dataset """
DataLoaderSaver().save_dataset(data, security_dataset, "processed")