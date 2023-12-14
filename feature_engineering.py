import pandas as pd
import matplotlib.pyplot as plt
import nltk
# import spacy

from DataLoaderSaver import DataLoaderSaver
from DataAnalyzer import DataAnalyzer
from DataProcessor import DataProcessor

""" Load processed dataset """
data = DataLoaderSaver().load_dataset("processed")

""" Create dataframe with necessary columns """
data = data[['Advisory ID','NCSC ID','Uitgiftedatum','Beschrijving', 'Kans','Schade']]

""" Create new column with the number of updates per NCSC ID """ ## column Versie differs in updates (either 2.00 or 1.01)
data = data.sort_values(by='Uitgiftedatum')
data = data.reset_index(drop=True)
data['Update'] = pd.Series(dtype='int')
NCSC_ids = []

for row in range(len(data)):
    if data.loc[row,'NCSC ID'] not in NCSC_ids:
        NCSC_ids.append(data.loc[row,'NCSC ID'])
        data.loc[row,'Update'] = 1
    elif data.loc[row,'NCSC ID'] in NCSC_ids:
        count = NCSC_ids.count(data.loc[row,'NCSC ID'])
        data.loc[row,'Update'] = count + 1
        NCSC_ids.append(data.loc[row,'NCSC ID'])

"""" NLP """
# nlp = spacy.load("nl_core_news_sm")
# doc = nlp(sentences[0])
# print(doc.text)
# for token in doc:
#     print(token.text, token.pos_, token.dep_)

""" Create new column with the number of words and tokens of each Beschrijving """
data['Words'] = pd.Series(dtype='int')
data['Tokens'] = pd.Series(dtype='int')

for row in range(len(data)):
    if type(data.loc[row,'Beschrijving']) == str:
        data.loc[row,'Words'] = len(data.loc[row,'Beschrijving'].split())
        data.loc[row,'Tokens'] = len(nltk.word_tokenize(data.loc[row,'Beschrijving']))
        # print(data.loc[row,'Beschrijving'].split())
        # print(nltk.word_tokenize(data.loc[row,'Beschrijving']))
    else:
        data.loc[row,'Words'] = 0
        data.loc[row,'Tokens'] = 0

print(data.head(10))

""" Save intermediate dataset """
DataLoaderSaver().save_dataset(data,"engineered", "$")

