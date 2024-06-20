import pandas as pd
import matplotlib.pyplot as plt

from DataLoaderSaver import DataLoaderSaver
from DataAnalyzer import DataAnalyzer
from DataProcessor import DataProcessor

""" Set dataset to run """
security_dataset = "APT"

""" Load initial dataset """
data = DataLoaderSaver().load_dataset(security_dataset, "initial")

""" General exploring of the dataset """
DataAnalyzer().print_column_names(data)
DataAnalyzer().print_info(data)
DataAnalyzer().check_duplicates(data)
DataAnalyzer().check_uniques(data)

""" Exploring specifics of the APT dataset using plots """
DataAnalyzer().print_histogram(data, "attack_vector")
