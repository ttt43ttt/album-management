# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 13:02:29 2020
@author: TianHx
检测人脸
"""

# %%
import random
import os
import time
import shutil
import pickle
import cv2
import face_recognition
import numpy as np
from imutils import paths
from sklearn import cluster, metrics
from centerface import CenterFace


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
def detect_face_by_haar(img) -> list:
    HAAR_CASCADE_FILE = r"C:\apps\Anaconda3\envs\py36_x86\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml"
    cascade = cv2.CascadeClassifier(HAAR_CASCADE_FILE)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    try:
        faces = cascade.detectMultiScale(img)
    except Exception as e:
        print(e)
        return []
    boxes = []
    for (x, y, w, h) in faces:
        # 转成上右下左
        boxes.append([y, x + w, y + h, x])
    return boxes


def detect_face_by_centerface(img) -> list:
    h, w = img.shape[:2]
    cf = CenterFace(landmarks=True)
    faces, landmarks = cf(img, h, w, threshold=0.5)
    boxes = []
    for face in faces:
        (x1, y1, x2, y2), score = face[:4], face[4]
        box = [int(y1), int(x2), int(y2), int(x1)]
        boxes.append(box)
    return boxes


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
        # boxes = detect_face_by_haar(image)
        # boxes = detect_face_by_centerface(image)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model=detect_model, number_of_times_to_upsample=0)
        print(f"detected {len(boxes)} faces")

        for (fi, box) in enumerate(boxes):
            (top, right, bottom, left) = box
            faceImg = image[top:bottom, left:right]
            # folder = os.path.join(destFolder, pName)
            folder = destFolder
            os.makedirs(folder, exist_ok=True)
            facePath = os.path.join(folder, f"{imageName}_{fi}.jpg")
            print(f"[INFO] writing to {facePath}")
            cv2.imwrite(facePath, faceImg)


# %%
srcFolder = r"C:\temp\images"
destFolder = r"C:\temp\faces-hog"
detect_model = "hog"  # hog or cnn

start = time.time()
detect_faces()
end = time.time()
print(f"detect_faces() takes {end - start} seconds")
