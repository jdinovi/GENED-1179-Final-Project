import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
import pandas as pd
import numpy as np
import collections
import tensorflow as tf
nltk.download('stopwords')
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

# Function to Remove Punctuation
def remove_punctuation(text):
  '''
  Input:
    'text': a string of characters
  Output:
    'text', but removed of punctuation
  '''
  text = str(text)
  for punc in string.punctuation:
      if punc in text:
          text = text.replace(punc, ' ')
  return text.strip()

# Function to Tokenize Text and Remove Stop Words from Text
def remove_stop_words_and_tokenize(text):
  '''
  Input: 
    'text': a string removed of punctuation
  Output: 
    Tokenized version of 'text' and with stop words removed
  '''
  text = text.lower()
  tokenized = word_tokenize(text)
  no_stops = []
  for word in tokenized:
    if word not in stop_words:
      no_stops.append(word)
  return no_stops

# Function to Stem Tokenized text
def stem(tokenized_text):
  '''
  Input: 
    'tokenized_text': a list of a tokenized feature
  Output: 
    Stemmed version of 'tokenized_text'
  '''
  for i, word in enumerate(tokenized_text):
    tokenized_text[i] = stemmer.stem(word)
  return tokenized_text

# Function to Lemmatize Tokenized text
def lemmatize(tokenized_text):
  '''
  Input: 
    'tokenized_text': a list of a tokenized feature
  Output: 
    Lemmatized version of 'tokenized_text'
  '''
  for i, word in enumerate(tokenized_text):
    tokenized_text[i] = lemmatizer.lemmatize(word)
  return tokenized_text

# ---------------------------------------------------------- #

# Function to Return Cleaned Text
def clean(text):
  '''
  Input: 
    'text': an input string
  Output: 
    'text' with removed punctuation, tokenized,
          stop words removed, and lemmatized
  '''
  text = remove_punctuation(text)
  text = remove_stop_words_and_tokenize(text)
  text = lemmatize(text)
  return text

# Implement Bag of Words Model
def build_set(feature_list):
  '''
  Input: 
    'feature_list': list of tuples of uncleaned input (0) text and sentiment (1)
  Output: 
    Set of all words in the combined and cleaned strings from 'feature_list'
  '''
  total_string = ""
  for feature in feature_list:
    if type(feature[0]) == type(" "):
      total_string += " " + feature[0]
  total_string = clean(total_string)
  return set(total_string)

# Function to Build a BoW Vector for a Given Feature and Set of Words
def build_vector(feature, word_set):
  '''
  Input:
    'feature'(list): a cleaned string of input
    'word_set'(set): a set of all clean words seen over all features
  Output:
    A bag of words vectorized version of a given feature
  '''
  vector = np.zeros((len(word_set),))
  if feature:
    word_counter = collections.Counter(feature)
    for i, word in enumerate(word_set):
      vector[i] += word_counter[word]
  return vector

def bow_matrix(feature_list, myset=None):
  '''
  Input:
    'feature_list': a list of features to train the model on
  Output:
    A matrix of the BoW representation of each feature
  '''
  if not myset:
    myset = build_set(feature_list)
  bow_mat = []
  y_vec = []
  for i, feature in enumerate(feature_list):
    y_vec.append(feature[1])
    feature = clean(feature[0])
    vector = build_vector(feature, myset)
    bow_mat.append(np.array(vector))
  return np.array(bow_mat), np.array(y_vec), myset

# Function to Handle the Data
def process_data(data):
  '''
  Input:
    'data': a pandas data frame with entries 'text' and 'sentiment'
  Output:
    A processed form of all the features with just the 'text' and 'sentiment'
    values zipped together
  '''
  out_text = []
  out_sents = []
  text = np.array(data['text'])
  sentiment = np.array(data['sentiment'])
  for i, sent in enumerate(sentiment):
    if sent == "positive":
      out_sents.append([0, 0, 1])
    elif sent == "neutral":
      out_sents.append([0, 1, 0])
    elif sent == "negative":
      out_sents.append([1, 0, 0])
    out_text.append(text[i])
  feature_list = zip(out_text, out_sents)
  return tuple(feature_list)


def get_model(size):
    feature_size = size
    input_dim = (feature_size,)
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(256, activation=tf.nn.relu, input_shape=input_dim),
        tf.keras.layers.Dense(256, activation=tf.nn.relu),
        tf.keras.layers.Dense(256, activation=tf.nn.relu),
        tf.keras.layers.Dense(3, activation=tf.nn.softmax)
    ])
    model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
    model.load_weights('network/saved_weights/')
    return model

if __name__ == '__main__':
  pass