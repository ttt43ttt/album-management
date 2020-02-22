# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 13:02:29 2020

@author: TianHx
"""

# %%
import random
import os
import shutil
import pickle
import cv2
import face_recognition
import numpy as np
from imutils import paths
from sklearn import cluster, metrics


# %%
def random_choose_test_data():
    "随机选择测试数据"
    # fromFolder = r"C:\code\github.com\datasets\FaceScrub\actresses\faces"
    fromFolder = r"C:\code\github.com\datasets\FaceScrub\actors\faces"
    destFolder = r"C:\code\github.com\datasets\FaceScrub-faces-10-100-01"
    numPersons = 5

    folders = os.listdir(fromFolder)
    random.shuffle(folders)

    for i in range(numPersons):
        folder = folders[i]
        shutil.copytree(os.path.join(fromFolder, folder),
                        os.path.join(destFolder, folder))


# %%
def encode_faces(faceFolder):
    "生成编码"
    faces = []
    persons = os.listdir(faceFolder)
    # 按人物目录遍历，生成labelId
    for (pIndex, pName) in enumerate(persons):
        folder = os.path.join(faceFolder, pName)
        imagePaths = paths.list_images(folder)
        for imagePath in imagePaths:
            # print(imagePath)
            face = {"labelId": pIndex, "imagePath": imagePath}
            faces.append(face)

    data = []
    # 遍历人脸
    for (i, face) in enumerate(faces):
        labelId = face['labelId']
        imagePath = face['imagePath']
        print("[INFO] processing image {}/{}".format(i + 1, len(faces)))
        print(imagePath)
        # load the input image and convert it from RGB (OpenCV ordering) to dlib ordering (RGB)
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        (h, w) = image.shape[:2]
        #(top, right, bottom, left)
        boxes = [(0, w, h, 0)]
        # compute the facial embedding for the face
        encodings = face_recognition.face_encodings(rgb, boxes)

        # build a dictionary of the image path, bounding box location,
        # and facial encodings for the current image
        d = [{
            "labelId": labelId,
            "imagePath": imagePath,
            "encoding": enc
        } for (box, enc) in zip(boxes, encodings)]
        data.extend(d)
    return data


# %%
def cluster_faces(data):
    encodings = [d["encoding"] for d in data]
    clt = cluster.DBSCAN(metric="euclidean", eps=0.5, min_samples=5, n_jobs=-1)
    clt.fit(encodings)
    return clt


# %%
testName = "FaceScrub-faces-10M-860-01"
faceFolder = f"C:\\code\\github.com\\datasets\\{testName}"
encodingsFile = f"C:\\code\\github.com\\datasets\\{testName}.encodings.pickle"

# %%
data = encode_faces(faceFolder)
pickle.dump(data, open(encodingsFile, "wb"))

# %%
data = pickle.load(open(encodingsFile, "rb"))

# %%
random.shuffle(data)
clt = cluster_faces(data)
labels_true = [d['labelId'] for d in data]
labels_pred = list(clt.labels_)
# print(labels_true)
# print(labels_pred)

fm_score = metrics.fowlkes_mallows_score(labels_true, labels_pred)
ar_score = metrics.adjusted_rand_score(labels_true, labels_pred)
ami_score = metrics.adjusted_mutual_info_score(labels_true, labels_pred)
(homo_score, comp_score,
 v_score) = metrics.homogeneity_completeness_v_measure(labels_true,
                                                       labels_pred)
print(
    f"fm_score: {fm_score}, ar_score: {ar_score}, ami_score: {ami_score}, homo_score: {homo_score}, comp_score: {comp_score}, v_score: {v_score}"
)

# %%
