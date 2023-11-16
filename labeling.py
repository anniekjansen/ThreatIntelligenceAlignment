import pandas as pd
import matplotlib.pyplot as plt

from DataSaverLoader import DataSaverLoader
from DataAnalyzer import DataAnalyzer
from DataProcessor import DataProcessor

""" Load initial dataset """
# data = DataAnalyzer().load_csv("NCSC_advisories.csv")
data = DataSaverLoader().load_dataset("dropped_data")

""" Create dataframe where NSCS IDs are not unique """
DataAnalyzer().check_uniques_columns(data, ['Advisory ID', 'NCSC ID'])

DataAnalyzer().print_selected_columns(data,['NCSC ID'])

data = data.loc[data.duplicated(subset=['NCSC ID'], keep=False)]
data = data.reset_index(drop=True)
print(data['NCSC ID'])

DataAnalyzer().print_selected_value(data, "NCSC ID", 'NCSC-2023-0023')

DataAnalyzer().check_uniques(data)
DataAnalyzer().check_uniques_columns(data, ['NCSC ID'])

data = data[['NCSC ID','Beschrijving']]

print(data)

# for loop > add column 0 (first advies), 1 (second advies), 2 (third advies), etc > based on uitgiftedatum preferably


