"""
Name : Sanket Meshram
Roll No. : 17CS30030
"""


import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB
import numpy
import spacy
nlp = spacy.load('en_core_web_md')


def remove_punctuation_and_lower(a):
    punctuations = '''!()-[]{};:'"\,<>+./?@#$%^&*_~'''
    a = a.lower()
    for x in punctuations:
        a = a.replace(x, "")
    return a


def read_train_and_preprocess():
    File = open("../data/train.tsv", "r")
    data = {"id": [], "text": [],  "hateful": []}
    File.readline()
    while True:
        line = File.readline()
        if len(line) == 0:
            break
        line = remove_punctuation_and_lower(line)
        line = line.split()
        data["id"].append(line[0])
        data["hateful"].append(int(line[-1]))
        data["text"].append(' '.join(line[1:-1]))

    return data["id"], data["text"], data["hateful"]


def read_test_and_preprocess():
    File = open("../data/test.tsv", "r")
    data = {"id": [], "text": []}
    File.readline()
    while True:
        line = File.readline()
        if len(line) == 0:
            break
        line = remove_punctuation_and_lower(line)
        line = line.split()
        data["id"].append(line[0])
        data["text"].append(' '.join(line[1:]))

    return data["id"], data["text"]




def test_train_to_TfIdf(train, test):

    vectorizer = TfidfVectorizer(max_df=.8, min_df=5)
    vectors = vectorizer.fit_transform(train)
    feature_names = vectorizer.get_feature_names()
    dense = vectors.todense()
    denselist = dense.tolist()
    train = numpy.array(denselist)

    vectors = vectorizer.transform(test)
    dense = vectors.todense()
    denselist = dense.tolist()
    test = numpy.array(denselist)
    return train, test

if __name__ == "__main__":



    id_train, x_train,  y_train = read_train_and_preprocess()
    id_test, x_test = read_test_and_preprocess()

    len_train = len(x_train)
    len_test = len(x_test)
    x_train_tfidf, x_test_tfidf = test_train_to_TfIdf(x_train, x_test)

    clf = MultinomialNB()
    clf.fit(x_train_tfidf, y_train)
    y_pred_RF = list(clf.predict(x_test_tfidf))

    y_pred_RF = pd.DataFrame(
        list(zip(id_test, y_pred_RF)), columns=['id', 'hateful'])
    y_pred_RF.to_csv("../predictions/T2.csv", index=False)


    pass
