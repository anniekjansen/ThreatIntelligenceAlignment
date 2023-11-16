import pandas as pd
import matplotlib.pyplot as plt

from DataSaverLoader import DataSaverLoader
# from DataAnalyzer import DataAnalyzer
from DataProcessor import DataProcessor

""" Load initial dataset """
data = DataSaverLoader().load_dataset("initial")
print(data)

""" Drop duplicates from the dataset """
data = DataProcessor().drop_duplicates(data)

""" Drop columns from the dataset """
# data = DataProcessing().drop_columns(data, ["Mogelijke oplossingen"])

""" Save intermediate dataset """
DataSaverLoader().save_dataset(data,"dropped_data")
