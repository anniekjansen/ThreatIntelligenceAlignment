import pandas as pd
import matplotlib.pyplot as plt

from DataLoaderSaver import DataLoaderSaver
# from DataAnalyzer import DataAnalyzer
from DataProcessor import DataProcessor

""" Load initial dataset """
data = DataLoaderSaver().load_dataset("initial")
print(data)

""" Drop duplicates from the dataset """
data = DataProcessor().drop_duplicates(data)

""" Drop columns from the dataset """
# data = DataProcessing().drop_columns(data, ["Mogelijke oplossingen"])

""" Change column Uitgiftedatum from object to datetime type """
data = DataProcessor().object_to_datetime(data)

""" Save intermediate dataset """
DataLoaderSaver().save_dataset(data,"processed")
