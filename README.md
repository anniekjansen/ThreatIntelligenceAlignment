# Code for Thesis

MSc Artificial Intelligence

Anniek Jansen

Included in this repository:

Classes:
* DataLoaderSaver.py: functions to load and save datasets
* DataAnalyzer.py: functions to analyze the dataset
* DataProcessor.py: functions to preprocess the dataset
* ClassificationEngineering.py: functions to create new classification columns
* URREFHelper.py: functions to populate the URREF ontology
* CompAnalyzer.py: functions to perform the comparative risk analyses

Pipeline:
* exploration_NCSC.py: exploratory data analysis of the NCSC dataset
* exploration_APT.py: exploratory data analysis of the APT dataset
* processing_NCSC.py: pre-processing of the NCSC dataset
* processing_APT.py: pre-processing of the APT dataset
* feature_engineering_NCSC.py: engineering of new attributes to the NCSC dataset
* classification_engineering.py: engineering of a new dataframe including four classification columns for the change Justification in NCSC descriptions
* RQ1.py: temporal analyses of threats
* RQ2.py: ontological analyses of threats
* RQ2_comp_analysis.py: comparative risk analyses


Extra files (excluded from final pipeline):
* DataScraper.py: functions to scrape data from the NCSC website
* data_scraping.py: scrape kans/schade data from web using NCSC IDs
* NLTKProcessor.py: functions to implement NLTK 
* nltk_processing.py: natural language processing of Beschrijving using NLTK
* spacy_processing.py: natural language processing of Beschrijving using Spacy
