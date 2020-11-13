"""
Name : Sanket Meshram
Roll No. : 17CS30030
"""

import fasttext
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
import numpy
import spacy
nlp = spacy.load('en_core_web_md')

def remove_punctuation_and_lower(a):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
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

def get_TfIdf(x):
    vectorizer = TfidfVectorizer(max_df=.8, min_df=.05)
    vectors = vectorizer.fit_transform(x)
    feature_names = vectorizer.get_feature_names()
    dense = vectors.todense()
    denselist = dense.tolist()
    df = pd.DataFrame(denselist, columns=feature_names)
    return df


def test_train_to_TfIdf(train, test):
    temp = train.copy() + test.copy()
    len_train = len(train)
    # print(temp[:10])
    now = get_TfIdf(temp)
    return now.iloc[:len_train].copy(), now.iloc[len_train:].copy()

def  get_Word2Vec(a):
    vector_size = 300
    ans = []
    for i in a : 
        ans.append(nlp(i).vector)
        if len(ans[-1]) == 0 :
            ans[-1] = [0 for _ in range(vector_size)]
    return ans
    pass

if __name__ == "__main__":

    id_train, x_train, y_train = read_train_and_preprocess()
    id_test, x_test = read_test_and_preprocess()

    len_train = len(x_train)
    len_test = len(x_test)

    ############################ PART - 1 #########################################    

    x_train_tfidf, x_test_tfidf = test_train_to_TfIdf(x_train, x_test)



    clf = RandomForestClassifier()
    clf.fit(x_train_tfidf, y_train)
    y_pred_RF = list(clf.predict(x_train_tfidf))

    y_pred_RF = pd.DataFrame(list(zip(id_test, y_pred_RF)), columns=['id', 'hateful'])

    y_pred_RF.to_csv("../predictions/RF.csv",index=False)
    
    ############################ PART - 1 #########################################

    ############################ PART - 2 #########################################

    x_train_Word2Vec = get_Word2Vec(x_train)
    x_test_Word2Vec =get_Word2Vec(x_test)
    clf = svm.SVC()
    clf.fit(x_train_Word2Vec, y_train)
    y_pred_SVM = list(clf.predict(x_test_Word2Vec))

    y_pred_SVM = pd.DataFrame(list(zip(id_test, y_pred_SVM)), columns=['id', 'hateful'])
    y_pred_SVM.to_csv("../predictions/SVM.csv", index=False)

    ############################ PART - 2 #########################################

    ############################ PART - 3 #########################################
    train_data_FastText = open("data.train.txt","w")
    for i in range(len(x_train)) :
        if y_train[i] :
            print("__label__positive",end = " ",file = train_data_FastText)
        else :
            print("__label__negative", end=" ", file=train_data_FastText)
        print(x_train[i], file=train_data_FastText)
    
    model = fasttext.train_supervised('data.train.txt')

    y_pred_FT = []

    for i in x_test :

        if model.predict(i)[0][0] == "__label__positive" :
            y_pred_FT.append(1)
        else :
            y_pred_FT.append(0)
    
    y_pred_SVM = pd.DataFrame(list(zip(id_test, y_pred_FT)), columns=['id', 'hateful'])
    y_pred_SVM.to_csv("../predictions/FT.csv", index=False)

    os.system("rm data.train.txt")
    ############################ PART - 3 #########################################



    

    
    pass
