# -*- coding: utf-8 -*-
"""Social Media Content.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1d6q4tVKKws4yQAwRcfvlfYIxG1KuzvRW
"""

from google.colab import drive
drive.mount('/content/drive')

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from pandas.core.common import random_state
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier

tds = pd.read_csv("/content/drive/MyDrive/Major project/True.csv")
fds = pd.read_csv("/content/drive/MyDrive/Major project/Fake.csv")

tds

class_true = ["Real"]*21417
tds["class_label"] = class_true
tds

fds

class_fake = ["Fake"]*23481
fds["class_label"] = class_fake
fds

tweets_dataset = pd.concat([tds,fds], axis=0)
tweets_dataset = tweets_dataset.sample(frac=1)#shuffled dataset
tweets_dataset.reset_index(inplace=True)
tweets_dataset

tweets_dataset.class_label.value_counts()

tweets_dataset["class_label_num"] = tweets_dataset["class_label"].map({"Fake":0,"Real":1})
tweets_dataset

#pip install spacy

import spacy
spacy.cli.download("en_core_web_lg")
nlp = spacy.load("en_core_web_lg")

nlp("Rohit Sharma's Team India will face Jos Buttler-led England in the second semifinal of the ICC men’s T20 World Cup 2022 at the Adelaide Oval on Thursday (November 10).\n Fans are hoping for a India vs Pakistan final, with Babar Azam's side already in the final after win over New Zealand on Wednesday (November 9). \nRohit Sharma’s side topped Super 12 Group 2 table with four wins in five games, their only loss coming against South Africa at Perth.\n\nEngland, on the other hand, finished second in Super 12 Group 1, losing to Ireland and their game against Australia was washed out without a ball being bowled.").vector

tweets_dataset["text_vec"]=tweets_dataset["text"].apply(lambda text: nlp(text).vector)
tweets_dataset

#tweets_dataset.to_csv("/content/drive/MyDrive/Fake_News_Detection/TweetsDataset.csv", index=False)
#tweetdata = pd.read_csv("/content/drive/MyDrive/Fake_News_Detection/TweetsDataset.csv")
#tweetdata

tweet_train, tweet_test, label_train, label_test = train_test_split(tweets_dataset.text_vec.values, tweets_dataset.class_label_num, test_size=0.2, random_state=2022)

tweet_train_2D = np.stack(tweet_train)
tweet_test_2D = np.stack(tweet_test)

"""
https://www.researchgate.net/post/what_are_the_different_algorithms_for_text_classification

Some Traditional ML Algorithms:
Logisitic Regression, Multinomial Naive Bayes, k Nearest Neighbors, Decision Tree and Support Vector Machine
Some Ensemble ML Algorithms are:
Adaboost, Random Forest, Bagging, Gradient Boosting etc
deep learning ones: 
Convolutional Neural Network (CNN), Long Short Term Modelr (LSTM), Recurrent Convolutional Neural Network (RCNN), etc
"""

mnb = MultinomialNB()
scaler = MinMaxScaler()
scaled_train = scaler.fit_transform(tweet_train_2D) #Negative values in data passed to MultinomialNB (input X)
scaled_test = scaler.transform(tweet_test_2D)
mnb.fit(scaled_train, label_train) # scaled to get positive range of numbers for pos & neg data

label_pred = mnb.predict(scaled_test)
print(classification_report(label_test, label_pred))

knn = KNeighborsClassifier(n_neighbors = 5, metric = "euclidean")
knn.fit(tweet_train_2D, label_train)

label_pred_knn = knn.predict(tweet_test_2D)
print(classification_report(label_test, label_pred_knn))

#lr = LogisticRegression()
#lr.fit(tweet_train_2D, label_train) #ConvergenceWarning: lbfgs failed to converge (status=1): STOP: TOTAL NO. of ITERATIONS REACHED LIMIT.

sv = svm.SVC()
sv.fit(tweet_train_2D, label_train)

label_pred_sv = sv.predict(tweet_test_2D)
print(classification_report(label_test, label_pred_sv))

randfor = RandomForestClassifier(max_depth=14, random_state=2022) # at max_depth 14, acc is max, no inc after that
#The random_state in these algorithms controls two randomized processes — bootstrapping of the samples when creating tress and getting a random subset of features to search for the best feature during the node splitting process when creating each tree.
randfor.fit(tweet_train_2D, label_train)

label_pred_randfor = randfor.predict(tweet_test_2D)
print(classification_report(label_test, label_pred_randfor))

