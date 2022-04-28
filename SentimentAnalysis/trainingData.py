# import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import sklearn.metrics as metrics


def getScore(data):
    score = []
    for i in range(len(data)):
        if data.iloc[i]['PosScore'] == 0:
            score.append(data.iloc[i]['NegScore'])
        else:
            score.append(data.iloc[i]['PosScore'])
    return score


# import word .txt dictionary for sentiment analysis './data/SentiWordNet_3.0.0.txt'
word_dict = pd.read_table('https://raw.githubusercontent.com/aesuli/SentiWordNet/master/data/SentiWordNet_3.0.0.txt', sep='\t', header=None,
                          names=['POS', 'ID',	'PosScore', 'NegScore', 'SynsetTerms', 'Gloss'])

# delete first 26 rows of data
word_dict = word_dict.iloc[26:]

# delete any row with NaN values
word_dict = word_dict.dropna()

# print(word_dict.head())

# train a sentiment analysis model using word_dict

score = getScore(word_dict)

# split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    word_dict['SynsetTerms'], score, test_size=0.4, random_state=0)

# create a pipeline
pipeline = Pipeline([
    # strings to token integer counts
    ('bow', CountVectorizer(analyzer='word')),
    # integer counts to weighted TF-IDF scores
    ('tfidf', TfidfTransformer()),
    # train on TF-IDF vectors w/ Naive Bayes classifier
    ('classifier', MultinomialNB()),
])
# train the model
model = pipeline.fit(X_train, y_train)
# make predictions
predicted = model.predict(X_test)
# calculate accuracy
accuracy = metrics.accuracy_score(y_test, predicted)
print('Accuracy: %s' % accuracy)

# create a classification report
classification_report = metrics.classification_report(
    y_test, predicted, zero_division=0)
print(classification_report)
