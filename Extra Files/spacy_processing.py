import spacy
import pandas as pd
import nltk

from DataLoaderSaver import DataLoaderSaver
from NLTKProcessor import TextProcessor
from DataProcessor import DataProcessor

""" Set dataset to run (NCSC/APT) """
security_dataset = "NCSC"
# security_dataset = "APT"

""" Load initial dataset """
data = DataLoaderSaver().load_dataset(security_dataset, "processed")

""" Load the Dutch Spacy language model """
nlp = spacy.load("nl_core_news_sm")
# nlp = spacy.load("en_core_web_sm")

""" Normalise unstructured text of Beschrijving attribute """
def preprocess_dutch_text(text):
    doc = nlp(text)
    tokens = [token.lemma_.lower().strip() for token in doc if token.lemma_ != "-PRON-"]
    return tokens

def add_nlp_features(dataframe, column_name):
    dataframe[f"{column_name}_tokens"] = dataframe[column_name].apply(preprocess_dutch_text)
    dataframe[f"{column_name}_pos"] = dataframe[column_name].apply(lambda x: [(token.text, token.pos_) for token in nlp(x)])
    dataframe[f"{column_name}_ner"] = dataframe[column_name].apply(lambda x: [(ent.text, ent.label_) for ent in nlp(x).ents])
    dataframe[f"{column_name}_bow"] = dataframe[column_name].apply(lambda x: dict([(token.lemma_, 1) for token in nlp(x)]))

def add_nlp_features_to_dataframe(data):
    add_nlp_features(data, "Beschrijving")

data = data.head(10)
add_nlp_features_to_dataframe(data)

for i in data['Beschrijving_ner']:
    print(i)

""" Save intermediate dataset """
DataLoaderSaver().save_dataset(data, security_dataset, "transformed")