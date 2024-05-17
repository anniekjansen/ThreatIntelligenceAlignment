# Code for Thesis

MSc Artificial Intelligence

Anniek Jansen

Included in this repository:

Classes:
* DataLoaderSaver.py: functions to load and save datasets
* DataAnalyzer.py: functions to analyze the dataset
* DataProcessor.py: functions to preprocess the dataset
* ClassificationEngineering.py: functions to create new classification columns

Pipeline:
* exploration.py: exploratory data analysis
* processing.py: pre-processing of the dataset
* feature_engineering.py: engineering of new columns to the original dataset
* classification_engineering.py: engineering of a new dataframe including four classification columns for the change in description

Extra files (excluded from final pipeline):
* DataScraper.py: functions to scrape data from the NCSC website
* data_scraping.py: scrape kans/schade data from web using NCSC IDs
* NLTKProcessor.py: functions to implement NLTK 
* nltk_processing.py: natural language processing of Beschrijving using NLTK
* spacy_processing.py: natural language processing of Beschrijving using Spacy
