import pandas as pd
import math
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk import ne_chunk
from sklearn.feature_extraction.text import CountVectorizer

from nltk.tag.perceptron import PerceptronTagger

class TextProcessor:

    def download_nltk_items(self):
        nltk.download('stopwords', 'dutch') #stopwords
        nltk.download('punkt', 'dutch') #punctuation
        nltk.download('omw-1.4', 'dutch') #lemmatizing
        nltk.download('averaged_perceptron_tagger', 'dutch') #POS tagging
        nltk.download('maxent_ne_chunker', 'dutch') #NER tagging
        nltk.download('words', 'dutch') #NER tagging
        stop_words = set(stopwords.words('dutch'))
        stemmer = SnowballStemmer('dutch')
        lemmatizer = WordNetLemmatizer()
        vectorizer = CountVectorizer()
        return stop_words, stemmer, lemmatizer, vectorizer

    def preprocess_text(self, text, stop_words):
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        tokens = word_tokenize(text)
        tokens = [word for word in tokens if word not in stop_words]
        return tokens

    def tokenize(self, text):
        tokens = word_tokenize(text)
        return tokens

    def stemming(self, tokens, stemmer):
        stemmed_tokens = [stemmer.stem(token) for token in tokens]
        return stemmed_tokens

    def lemmatizing(self, tokens, lemmatizer):
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
        return lemmatized_tokens
    
    def pos_tagging(self, tokens):
        pos_tagging = nltk.pos_tag(tokens)
        return pos_tagging

    def ner_tagging(self, pos_tagging):
        ner_tagging = ne_chunk(pos_tagging)
        return ner_tagging

    def bag_of_words(self, tokens, vectorizer):
        bag_of_words = vectorizer.fit_transform([u' '.join(tokens)])
        return bag_of_words