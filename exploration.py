import pandas as pd
import matplotlib.pyplot as plt

from DataLoaderSaver import DataLoaderSaver
from DataAnalyzer import DataAnalyzer
# from DataProcessor import DataProcessor

""" Load initial dataset """
data = DataLoaderSaver().load_dataset("initial")
# print(data)

""" Exploring the dataset """
# DataAnalyzer().print_column_names(data)
DataAnalyzer().print_info(data)
# DataAnalyzer().print_histogram(data, "Kans")
# DataAnalyzer().print_histogram(data, "Schade")
DataAnalyzer().print_barchart_kans_schade(data)
# DataAnalyzer().print_selected_columns(data, ["Titel","NCSC ID","Advisory ID"])
# DataAnalyzer().print_selected_cell(data, 1, "Schadeomschrijving")
# DataAnalyzer().print_selected_value(data, "NCSC ID", 'NCSC-2023-0023')
# DataAnalyzer().print_selected_cell(data, 11806, "NCSC ID")
# DataAnalyzer().print_selected_cell(data, 0, "NCSC ID")

""" Check for duplicates in the dataset """
DataAnalyzer().check_duplicates(data)
# DataAnalyzer().check_duplicates_columns(data, ['Advisory ID', 'NCSC ID'])

""" Check for unique values in the dataset """
DataAnalyzer().check_uniques(data)
# DataAnalyzer().check_uniques_columns(data, ['Advisory ID', 'NCSC ID'])


