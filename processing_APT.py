import pandas as pd
import matplotlib.pyplot as plt

from DataLoaderSaver import DataLoaderSaver
from DataAnalyzer import DataAnalyzer
from DataProcessor import DataProcessor

""" Set dataset to run """
security_dataset = "APT"

""" Load initial dataset """
data = DataLoaderSaver().load_dataset(security_dataset, "initial")
data = data.reset_index()
print(data.head())

""" Delete duplicates and missing values from the dataset """
data = DataProcessor().drop_duplicates(data)
data = DataProcessor().drop_missing_values(data)

""" Delete irrelevant columns from the dataset """
data = DataProcessor().drop_columns(data, ["APT"])
data = data.reset_index(drop=True)

""" Change time columns from object to datetime type """
data = DataProcessor().object_to_datetime(data, 'exploited_time')
data = DataProcessor().object_to_datetime(data, 'published_time')
data = DataProcessor().object_to_datetime(data, 'reserved_time')

""" Save intermediate dataset """
DataLoaderSaver().save_dataset(data, security_dataset, "processed")