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
import dlib
import face_recognition
import numpy as np
from imutils import paths
from sklearn import cluster, metrics


# %%
def random_choose_test_data():
    """随机选择测试数据"""
    # fromFolder = r"C:\datasets\FaceScrub\actors\faces"
    # fromFolder = r"C:\datasets\FaceScrub\actresses\faces"
    fromFolder = r"C:\datasets\FaceScrub-faces"
    destFolder = r"C:\datasets\face-tests\FaceScrub-faces-mix-10-05"
    numPersons = 10

    folders = os.listdir(fromFolder)
    random.shuffle(folders)

    for i in range(numPersons):
        folder = folders[i]
        shutil.copytree(os.path.join(fromFolder, folder),
                        os.path.join(destFolder, folder))


# %%
def encode_faces(faceFolder):
    """生成编码"""
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
        # (top, right, bottom, left)
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
def cluster_faces_by_DBSCAN(data, eps=0.5, min_samples=5):
    encodings = [d["encoding"] for d in data]
    clt = cluster.DBSCAN(metric="euclidean", eps=eps, min_samples=min_samples, n_jobs=-1)
    clt.fit(encodings)

    # labelIDs = np.unique(clt.labels_)
    # numUniqueFaces = len(np.where(labelIDs > -1)[0])

    labels = list(clt.labels_)
    for (i, label) in enumerate(labels):
        if label == -1:
            # -1是噪声点，表明没有所属的cluster，单独给一个标签
            labels[i] = len(labels) + i
    return labels


def cluster_faces_by_CW(data, threshold=0.5):
    encodings = [dlib.vector(d["encoding"]) for d in data]
    labels = dlib.chinese_whispers_clustering(encodings, threshold)
    return labels


def cluster_faces_by_OPTICS(data):
    encodings = [d["encoding"] for d in data]
    clt = cluster.OPTICS(cluster_method="xi", max_eps=2, min_samples=5, metric="euclidean", n_jobs=-1)
    clt.fit(encodings)

    # print(clt.core_distances_)
    labels = list(clt.labels_)
    for (i, label) in enumerate(labels):
        if label == -1:
            # -1是噪声点，表明没有所属的cluster，单独给一个标签
            labels[i] = len(labels) + i
    return labels


def cluster_faces_by_Agglomerative(data, threshold=1.0):
    encodings = [d["encoding"] for d in data]
    clt = cluster.AgglomerativeClustering(distance_threshold=threshold, n_clusters=None)
    clt.fit(encodings)
    # print(clt.labels_)
    return clt.labels_


# %%
# testName = "FaceScrub-faces-10-100-01"

# testName = "FaceScrub-faces-10M-860-01"
# testName = "FaceScrub-faces-10F-678-01"
# testName = "FaceScrub-faces-5M5F-892-01"

# testName = "FaceScrub-faces-20M-1852-01"
# testName = "FaceScrub-faces-20F-1622-01"
# testName = "FaceScrub-faces-10M10F-1677-01"

# testName = "FaceScrub-faces-mix-10-01"

# testName = "CASIA-FaceV5(000-099)-faces-hog"

# testName = "JAFFE-faces-hog"
# testName = "JAFFE-faces-cnn"

# testName = "THWP-faces-hog"
testName = "rotate-test"

faceFolder = f"C:\\datasets\\face-tests\\{testName}"
encodingsFile = f"C:\\datasets\\face-tests\\{testName}.encodings.pickle"

re_encode_faces = False

# %%
# 开始人脸编码
data = None
if os.path.exists(encodingsFile):
    data = pickle.load(open(encodingsFile, "rb"))
if data is None or re_encode_faces:
    data = encode_faces(faceFolder)
    pickle.dump(data, open(encodingsFile, "wb"))


# %%
def evaluate():
    def p(name, score):
        print(f"{name}: {round(score, 4)}")

    fm_score = metrics.fowlkes_mallows_score(labels_true, labels_pred)
    ar_score = metrics.adjusted_rand_score(labels_true, labels_pred)
    # ami_score = metrics.adjusted_mutual_info_score(labels_true, labels_pred)
    (homo_score, comp_score,
     v_score) = metrics.homogeneity_completeness_v_measure(labels_true,
                                                           labels_pred)

    # no true labels
    # encodings = [d["encoding"] for d in data]
    # silhouette_score = metrics.silhouette_score(encodings, labels_pred, metric='euclidean')
    # davies_bouldin_score = metrics.davies_bouldin_score(encodings, labels_pred)

    # p("fm_score", fm_score)
    # p("ar_score", ar_score)
    # p("ami_score", ami_score)
    # p("homo_score", homo_score)
    # p("comp_score", comp_score)
    # p("v_score", v_score)

    # homogeneity: each cluster contains only members of a single class.
    # completeness: all members of a given class are assigned to the same cluster.
    # print(f"{round(paramx, 4)}\t{round(fm_score, 4)}\t{round(ar_score, 4)}\t{round(homo_score, 4)}\t{round(comp_score, 4)}\t{round(v_score, 4)}")
    print(f"{round(paramx, 4)}\t{round(ar_score, 4)}")


# %%
# 多个聚类参数测试
random.shuffle(data)

for paramx in np.arange(0.2, 0.7, 0.01):
    labels_pred = cluster_faces_by_DBSCAN(data, eps=paramx, min_samples=1)
    # labels_pred = cluster_faces_by_CW(data, threshold=paramx)
    # labels_pred = cluster_faces_by_Agglomerative(data, threshold=paramx)
    # for paramx in range(1, 50):
    #     labels_pred = cluster_faces_by_DBSCAN(data, eps=0.5, min_samples=paramx)
    labels_true = [d['labelId'] for d in data]
    # print(labels_true)
    # print(labels_pred)
    evaluate()

# %%
# 聚类并且评价
random.shuffle(data)
labels_pred = cluster_faces_by_Agglomerative(data, threshold=1.5)
print(labels_pred)
labels_true = [d['labelId'] for d in data]
ar_score = metrics.adjusted_rand_score(labels_true, labels_pred)
print(f"{round(ar_score, 4)}")
