# %%
import os
import pickle
import random
import numpy as np
import dlib
from sklearn import cluster, metrics


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


def cluster_faces_by_Agglomerative(data, threshold=1.0):
    encodings = [d["encoding"] for d in data]
    clt = cluster.AgglomerativeClustering(distance_threshold=threshold, n_clusters=None)
    clt.fit(encodings)
    # print(clt.labels_)
    return clt.labels_


# %%
testName = "THWP-faces-hog"

faceFolder = f"C:\\datasets\\face-tests\\{testName}"
encodingsFile = f"C:\\datasets\\face-tests\\{testName}.encodings.pickle"

data = pickle.load(open(encodingsFile, "rb"))

# %%
random.shuffle(data)
labels_true = [d['labelId'] for d in data]

# labels_pred = cluster_faces_by_Agglomerative(data, threshold=1.5)
# print(labels_pred)
# ar_score = metrics.adjusted_rand_score(labels_true, labels_pred)
# print(f"{round(ar_score, 4)}")

# 建立图片中的人脸列表 {imgID: [faceIndex,...]}
imgFaceDict = {}
for (index, d) in enumerate(data):
    faceImgPath = d['imagePath']
    imgName = os.path.basename(faceImgPath)
    imgID = imgName.split("_")[0]
    if imgID in imgFaceDict:
        faces = imgFaceDict[imgID]
    else:
        faces = []
        imgFaceDict[imgID] = faces
    faces.append(index)

# 含有2个或以上人脸的照片作为限制条件 [[face1, face2], [face3,face4], ...]
restrictFacesList = []
for imgID, faces in imgFaceDict.items():
    if len(faces) > 1:
        restrictFacesList.append(faces)


# 计算限制条件被违反的照片个数（比例）
# violateCount = 0
# for restrictFaces in restrictFacesList:
#     # restrictFaces是一张照片中出现的人脸列表，它们不应该出现在同一个cluster里
#     personLabelSet = set()
#     for faceIndex in restrictFaces:
#         label = labels_pred[faceIndex]
#         personLabelSet.add(label)
#     if len(personLabelSet) < len(restrictFaces):
#         # 类簇个数少于人脸数，说明有的人脸被聚在了一个cluster里
#         violateCount += 1
#
# violateRate = float(violateCount) / len(restrictFacesList)
# print(f'违反限制{violateCount}/{len(restrictFacesList)} = {round(violateRate, 4)}')

# %%
def faces_distance_in_photo():
    """查看同一张照片中人脸之间的距离分布情况"""
    encodings = [d["encoding"] for d in data]

    def min_distance(faces):
        """人脸之间的最小距离"""
        minDist = 10
        for i in range(len(faces)):
            f1 = encodings[faces[i]]
            for j in range(i + 1, len(faces)):
                f2 = encodings[faces[j]]
                # 计算距离
                dist = np.linalg.norm(f1 - f2)
                if dist < minDist:
                    minDist = dist
        return minDist

    for faces in restrictFacesList:
        minDist = min_distance(faces)
        print(minDist)


# %%
def checkViolate(restrictFacesList, labels_pred):
    # 计算限制条件被违反的照片个数（比例）
    violateCount = 0
    for restrictFaces in restrictFacesList:
        # restrictFaces是一张照片中出现的人脸列表，它们不应该出现在同一个cluster里
        personLabelSet = set()
        for faceIndex in restrictFaces:
            label = labels_pred[faceIndex]
            personLabelSet.add(label)
        if len(personLabelSet) < len(restrictFaces):
            # 类簇个数少于人脸数，说明有的人脸被聚在了一个cluster里
            violateCount += 1

    violateRate = round(float(violateCount) / len(restrictFacesList), 4)
    # print(f'违反限制{violateCount}/{len(restrictFacesList)} = {violateRate}')
    return violateRate


for paramx in np.arange(0.2, 0.5, 0.01):
    # labels_pred = cluster_faces_by_Agglomerative(data, threshold=paramx)
    # labels_pred = cluster_faces_by_DBSCAN(data, eps=paramx, min_samples=1)
    labels_pred = cluster_faces_by_CW(data, threshold=paramx)

    ar_score = metrics.adjusted_rand_score(labels_true, labels_pred)
    violateRate = checkViolate(restrictFacesList, labels_pred)
    print(f"{round(paramx, 4)}\t{violateRate}\t{round(ar_score, 4)}")
