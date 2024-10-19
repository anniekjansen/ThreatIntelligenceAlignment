# Threat Intelligence Alignment

MSc Artificial Intelligence

Anniek Jansen

Included in this repository:

Classes:
* DataLoaderSaver.py: functions to load and save datasets
* DataAnalyzer.py: functions to analyze the dataset
* DataProcessor.py: functions to preprocess the dataset
* ClassificationEngineering.py: functions to create new classification columns
* URREFHelper.py: functions to populate the URREF ontology
* ChartCreator.py: functions to create different charts.
* CompAnalyzer.py: functions to perform the comparative risk analyses

Pipeline:
* exploration_NCSC.py: exploratory data analysis of the NCSC dataset
* exploration_APT.py: exploratory data analysis of the APT dataset
* processing_NCSC.py: pre-processing of the NCSC dataset
* processing_APT.py: pre-processing of the APT dataset
* feature_engineering_NCSC.py: engineering of new attributes to the NCSC dataset
* classification_engineering.py: engineering of a new dataframe including four classification columns for the change Justification in NCSC descriptions
* RQ1.py: temporal analysis of threats
* RQ2.py: ontological analysis of threats
* RQ2_charts.py: charts for ontological analysis
* RQ2_comp_analysis.py: comparative risk analyses

Further directories:
* SPARQL Queries: SPARQL queries for ontological analysis, including results for comparative risk analyses


Extra Files (excluded from final pipeline):
* DataScraper.py: functions to scrape data from the NCSC website
* data_scraping.py: scrape kans/schade data from web using NCSC IDs
* NLTKProcessor.py: functions to implement NLTK 
* nltk_processing.py: natural language processing of Beschrijving using NLTK
* spacy_processing.py: natural language processing of Beschrijving using Spacy
