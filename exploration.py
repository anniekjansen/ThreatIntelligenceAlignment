import pandas as pd
import matplotlib.pyplot as plt

from DataLoaderSaver import DataLoaderSaver
from DataAnalyzer import DataAnalyzer
# from DataProcessor import DataProcessor

""" Set dataset to run (NCSC/APT) """
security_dataset = "NCSC"
# security_dataset = "APT"

""" Load initial dataset """
data = DataLoaderSaver().load_dataset(security_dataset, "initial")

""" General exploring of the dataset """
DataAnalyzer().print_column_names(data)
DataAnalyzer().print_info(data)
DataAnalyzer().check_duplicates(data)
DataAnalyzer().check_uniques(data)

""" Exploring the NCSC dataset """
# DataAnalyzer().print_histogram(data, "Kans")
# DataAnalyzer().print_histogram(data, "Schade")
# DataAnalyzer().print_barchart_kans_schade(data)
# DataAnalyzer().print_selected_columns(data, ["Titel","NCSC ID","Advisory ID"])
# DataAnalyzer().print_selected_cell(data, 1, "Schadeomschrijving")
# DataAnalyzer().print_selected_value(data, "NCSC ID", 'NCSC-2023-0023')
# DataAnalyzer().print_selected_cell(data, 11806, "NCSC ID")
# DataAnalyzer().print_selected_cell(data, 0, "NCSC ID")
# DataAnalyzer().check_duplicates_columns(data, ['Advisory ID', 'NCSC ID'])
# DataAnalyzer().check_uniques_columns(data, ['Advisory ID', 'NCSC ID'])

""" Exploring the APT dataset """
# DataAnalyzer().print_histogram(data, "attack_vector")