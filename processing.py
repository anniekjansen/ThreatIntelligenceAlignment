import pandas as pd
import matplotlib.pyplot as plt

from DataLoaderSaver import DataLoaderSaver
# from DataAnalyzer import DataAnalyzer
from DataProcessor import DataProcessor

""" Load initial dataset """
data = DataLoaderSaver().load_dataset("initial")

""" Delete duplicates from the dataset """
data = DataProcessor().drop_duplicates(data)

""" Delete unimportant columns from the dataset """
# data = DataProcessing().drop_columns(data, ["Mogelijke oplossingen"])

""" Delete rows where NCSC ID does not occure more than once """
data = data.loc[data.duplicated(subset=['NCSC ID'], keep=False)]
data = data.reset_index(drop=True)

""" Change column Uitgiftedatum from object to datetime type """
data = DataProcessor().object_to_datetime(data)

""" Save intermediate dataset """
DataLoaderSaver().save_dataset(data,"processed")

# print(data)
