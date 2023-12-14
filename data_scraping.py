import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait

from DataLoaderSaver import DataLoaderSaver
from DataAnalyzer import DataAnalyzer
from DataScraper import DataScraper

""" Load processed dataset """
data = DataLoaderSaver().load_dataset("processed")

""" Create list with valid NCSC_IDs from dataset """
print(data['NCSC ID'].unique())
NCSC_IDs = data['NCSC ID'].unique().tolist()

# print(NCSC_IDs)

""" Scrape data and save as new column in dataset """

for NCSC_ID in NCSC_IDs:
    if "GOVCERT" not in NCSC_ID:
        URL = DataScraper().url_maker(NCSC_ID)

        soup = DataScraper().load_beautifulsoup(URL)

        if soup:
            kans_dict = DataScraper().scrape_data(soup, "kans")
            schade_dict = DataScraper().scrape_data(soup, "schade")

            data['kans_dict'] = dict()
            data['schade_dict'] = dict()

            data.loc[data['NCSC ID'] == NCSC_ID, ['kans_dict','schade_dict']] = [kans_dict, schade_dict]

# print(data)
DataAnalyzer().print_selected_columns(data, ["NCSC ID","kans_dict", "schade_dict"])

""" Save intermediate dataset """
DataLoaderSaver().save_dataset(data,"scraped")
