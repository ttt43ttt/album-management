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
# {labelId: [encoding1, encoding2, ...]}
dataLabelMap = {}
for d in data:
    label = d['labelId']
    if label in dataLabelMap:
        faces = dataLabelMap[label]
    else:
        faces = []
        dataLabelMap[label] = faces
    faces.append(d['encoding'])

# %%
def max_distance(encodings):
    """人脸之间的最大距离"""
    maxDist = 0
    for i in range(len(encodings)):
        f1 = encodings[i]
        for j in range(i + 1, len(encodings)):
            f2 = encodings[j]
            # 计算距离
            dist = np.linalg.norm(f1 - f2)
            if dist > maxDist:
                maxDist = dist
    return maxDist

for label, encodings in dataLabelMap.items():
    # encodings是同一个人的人脸编码
    maxDist = max_distance(encodings)
    print(f'{label}\t{round(maxDist,5)}')

# %%
