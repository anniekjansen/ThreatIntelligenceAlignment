import pandas as pd
import matplotlib.pyplot as plt

import seaborn as sns

from DataLoaderSaver import DataLoaderSaver
from DataProcessor import DataProcessor

""" Set dataset to run (NCSC/APT) """
security_dataset = "NCSC"
# security_dataset = "APT"

""" Load initial dataset """
data = DataLoaderSaver().load_dataset(security_dataset, "initial")

""" Delete duplicates from the dataset """
data = DataProcessor().drop_duplicates(data)

""" Delete irrelevant columns from the dataset """
data = DataProcessor().drop_columns(data, ["NCSC inschaling","Versie"])

""" Delete rows where NCSC ID does not occure more than once """
data = data.loc[data.duplicated(subset=['NCSC ID'], keep=False)]
data = data.reset_index(drop=True)

""" Change column Uitgiftedatum from object to datetime type """
data = DataProcessor().object_to_datetime(data)

""" Save intermediate dataset """
DataLoaderSaver().save_dataset(data, security_dataset, "processed")

# print(print(data.dtypes))

# sns.boxplot(data['Advisory ID'])
# plt.show()

data.set_index('Uitgiftedatum', inplace=True)
grouped = data.groupby(data.index.year).size()

# Create a new dataframe with the date and count as columns
count_df = pd.DataFrame({'year': grouped.index, 'count': grouped.values})

# Plot the count of instances for each date as a bar plot
# count_df.plot(kind='bar', x='year', y='count')
count_df.plot(kind='line', x='year', y='count')

# Set title and labels for axes
plt.title('Line plot of the Instances per Year')
plt.xlabel('Year')
plt.ylabel('Count')

plt.show()
plt.savefig('lineplot_Uitgiftedatum.png')
# plt.close()