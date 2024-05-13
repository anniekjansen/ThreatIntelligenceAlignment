import pandas as pd
import nltk

from DataLoaderSaver import DataLoaderSaver
from NLTKProcessor import NLTKProcessor
from DataProcessor import DataProcessor

""" Set dataset to run (NCSC/APT) """
security_dataset = "NCSC"
# security_dataset = "APT"

""" Load initial dataset """
data = DataLoaderSaver().load_dataset(security_dataset, "processed")

""" Normalise unstructured text of Beschrijving attribute """
stop_words, stemmer, lemmatizer, vectorizer = NLTKProcessor().download_nltk_items()

data = data.head(100)

def text_preprocessing(row):
    if pd.notna(row['Beschrijving']):
        row['Tokenized'] = NLTKProcessor().preprocess_text(row['Beschrijving'], stop_words)
        # row['Tokenized'] = NLTKProcessor().tokenize(row['Beschrijving'])
        row['Stemmed'] = NLTKProcessor().stemming(row['Tokenized'], stemmer)
        row['Lemmatized'] = NLTKProcessor().lemmatizing(row['Tokenized'], lemmatizer)
        row['POS-tag'] = NLTKProcessor().pos_tagging(row['Tokenized'])
        row['NER-tag'] = NLTKProcessor().ner_tagging(row['POS-tag'])
        row['BOW-tag'] = NLTKProcessor().bag_of_words(row['Tokenized'], vectorizer)
    return row

data = data.apply(text_preprocessing, axis=1)

for i in data['NER-tag']:
    print(i)

""" Save intermediate dataset """
DataLoaderSaver().save_dataset(data, security_dataset, "transformed")
