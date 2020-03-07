# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 13:02:29 2020
@author: TianHx
检测人脸
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
def rotateImage(img, angle):
    code = None
    if angle == 90:
        code = cv2.ROTATE_90_COUNTERCLOCKWISE
    elif angle == 180:
        code = cv2.ROTATE_180
    elif angle == 270:
        code = cv2.ROTATE_90_CLOCKWISE
    rotated = cv2.rotate(img, code)
    return rotated


# %%
def detect_faces():
    """检测人脸，并按人物文件夹存成文件"""
    persons = []
    personFolders = os.listdir(srcFolder)
    # 按人物目录遍历，生成labelId
    for (pIndex, pName) in enumerate(personFolders):
        folder = os.path.join(srcFolder, pName)
        imagePaths = paths.list_images(folder)
        for imagePath in imagePaths:
            # print(imagePath)
            person = {"name": pName, "imagePath": imagePath}
            persons.append(person)

    for (i, person) in enumerate(persons):
        pName = person['name']
        imagePath = person['imagePath']
        imageName = os.path.splitext(os.path.basename(imagePath))[0]
        print("[INFO] processing image {}/{}".format(i + 1, len(persons)))
        print(imagePath)

        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model=detect_model)
        print(f"detected {len(boxes)} faces")

        for (fi, box) in enumerate(boxes):
            (top, right, bottom, left) = box
            faceImg = image[top:bottom, left:right]
            folder = os.path.join(destFolder, pName)
            os.makedirs(folder, exist_ok=True)
            facePath = os.path.join(folder, f"{imageName}_{fi}.jpg")
            print(f"[INFO] writing to {facePath}")
            cv2.imwrite(facePath, faceImg)


# %%
srcFolder = r"C:\datasets\face-tests\rotate-test"
destFolder = r"C:\temp\rotate-test"
detect_model = "hog"  # hog or cnn

detect_faces()
