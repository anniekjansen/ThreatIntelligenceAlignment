import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from DataLoaderSaver import DataLoaderSaver
from DataAnalyzer import DataAnalyzer
from DataProcessor import DataProcessor

""" Set dataset to run """
security_dataset = "APT"

""" Load initial dataset """
data = DataLoaderSaver().load_dataset(security_dataset, "initial")
data = data.reset_index()
# print(data.head())

""" Data Selection """

""" Delete duplicates from the dataset """
data = DataProcessor().drop_duplicates(data)
data = DataProcessor().drop_missing_values(data)

""" Delete irrelevant columns from the dataset """
# print(data['update'].value_counts()["*"])
# print(data['update'].unique())
data = DataProcessor().drop_columns(data, ["APT", "update"])
data = data.reset_index(drop=True)
print(data.shape)

""" Data Cleaning """

""" Change time columns from string object to datetime type """
# DataAnalyzer().check_column_types(data)
data = DataProcessor().object_to_datetime(data, 'exploited_time')
data = DataProcessor().object_to_datetime(data, 'published_time')
data = DataProcessor().object_to_datetime(data, 'reserved_time')

""" Create lineplot with time columns """
fig, ax = plt.subplots(figsize=(10, 6))

exploited_counts = data['exploited_time'].dt.year.value_counts().sort_index()
published_counts = data['published_time'].dt.year.value_counts().sort_index()
reserved_counts = data['reserved_time'].dt.year.value_counts().sort_index()

ax.plot(exploited_counts.index, exploited_counts.values, label='Exploited')
ax.plot(published_counts.index, published_counts.values, label='Published')
ax.plot(reserved_counts.index, reserved_counts.values, label='Reserved')

ax.set_title('Count per Year')
ax.set_xlabel('Year')
ax.set_ylabel('Count')
ax.legend()
ax.grid(True)

# plt.savefig('lineplotTimeAPT.png')
plt.show()

""" Cclean input to None if applicable """
data = DataProcessor().values_to_None(data, ['version', "os"])

""" Save intermediate dataset """
DataLoaderSaver().save_dataset(data, security_dataset, "processed")
