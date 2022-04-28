# sentiment analysis on ./data folder using each csv as a point in time

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


def sentiment_analysis(data):
    # define pipeline
    pipeline = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', MultinomialNB()),
    ])

    # define X and y
    X = data['text']
    y = data['label']

    # split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    # fit pipeline to training data
    pipeline.fit(X_train, y_train)

    # predict on test data
    y_pred = pipeline.predict(X_test)

    # print accuracy
    print('Accuracy:', metrics.accuracy_score(y_test, y_pred))

    # print confusion matrix
    print('Confusion matrix:')
    print(metrics.confusion_matrix(y_test, y_pred))

    # print classification report
    print('Classification report:')
    print(metrics.classification_report(y_test, y_pred))


if __name__ == '__main__':
    # import data into DataFrames
    data = pd.read_csv('./data/1_China_Shanghai_Death.csv', encoding='latin-1')
    sentiment_analysis(data)
