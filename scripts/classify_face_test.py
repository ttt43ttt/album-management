# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 13:02:29 2020

@author: TianHx
"""
# %%
import os
import pickle
import random
import numpy as np
import dlib
from sklearn import cluster, metrics
from sklearn import model_selection
from sklearn import neighbors
from sklearn import svm

# %%
testName = "THWP-faces-hog"

faceFolder = f"C:\\datasets\\face-tests\\{testName}"
encodingsFile = f"C:\\datasets\\face-tests\\{testName}.encodings.pickle"

data = pickle.load(open(encodingsFile, "rb"))

# %%
X = [d["encoding"] for d in data]
y = [d["labelId"] for d in data]

# %%
# KNN分类器
for i in range(20):
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.3)

    # weights="distance"
    clf = neighbors.KNeighborsClassifier(n_neighbors=5, weights="distance", n_jobs=-1)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    score1 = metrics.accuracy_score(y_true=y_test, y_pred=y_pred)

    # weights="uniform"
    clf = neighbors.KNeighborsClassifier(n_neighbors=5, weights="uniform", n_jobs=-1)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    score2 = metrics.accuracy_score(y_true=y_test, y_pred=y_pred)
    print(f'{i + 1}\t{round(score1, 4)}\t{round(score2, 4)}')

# %%
# SVM分类器
for i in range(10):
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.3)
    clf = svm.SVC(gamma='auto')
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    score = metrics.accuracy_score(y_true=y_test, y_pred=y_pred)
    print(f'{i + 1}\t{round(score, 4)}')
