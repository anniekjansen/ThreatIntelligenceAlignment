import pandas as pd
import matplotlib.pyplot as plt

from DataSaverLoader import DataSaverLoader
from DataAnalyzer import DataAnalyzer
from DataProcessing import DataProcessing

""" Load initial dataset """
# data = DataAnalyzer().load_csv("NCSC_advisories.csv")
data = DataSaverLoader().load_dataset("initial")
print(data)

""" Exploring the dataset """
# DataAnalyzer().print_column_names(data)
# DataAnalyzer().print_info(data)
# DataAnalyzer().print_histogram(data, "Kans")
# DataAnalyzer().print_selected_columns(data, ["Titel","NCSC ID","Advisory ID"])
# DataAnalyzer().print_selected_cell(data, 1, "Mogelijke oplossingen")
# DataAnalyzer().print_selected_value(data, "Advisory ID", 32000)
# DataAnalyzer().print_selected_cell(data, 11806, "NCSC ID")
# DataAnalyzer().print_selected_cell(data, 0, "NCSC ID")

""" Check for duplicates in the dataset """
# DataAnalyzer().check_duplicates(data)
# DataAnalyzer().check_duplicates_columns(data, ['Advisory ID', 'NCSC ID'])

""" Check for unique values in the dataset """
# DataAnalyzer().check_uniques(data)

""" Drop duplicates from the dataset """
data = DataProcessing().drop_duplicates(data)

""" Drop columns from the dataset """
# data = DataProcessing().drop_columns(data, ["Mogelijke oplossingen"])
# print(data)

""" Save intermediate dataset """
DataSaverLoader().save_dataset(data,"dropped_data")




