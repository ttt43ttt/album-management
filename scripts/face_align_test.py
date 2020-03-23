# %%
import random
import os
import shutil
import time
import pickle
import cv2
import face_recognition_models
import dlib
import face_recognition
import numpy as np
from imutils import paths
from sklearn import cluster, metrics

# %%

face_detector = dlib.get_frontal_face_detector()

predictor_68_point_model = face_recognition_models.pose_predictor_model_location()
pose_predictor_68_point = dlib.shape_predictor(predictor_68_point_model)

predictor_5_point_model = face_recognition_models.pose_predictor_five_point_model_location()
pose_predictor_5_point = dlib.shape_predictor(predictor_5_point_model)


# %%
def align_face(face_image):
    # pose_predictor = pose_predictor_5_point
    pose_predictor = pose_predictor_68_point
    (h, w) = face_image.shape[:2]
    face_location = dlib.rectangle(0, 0, w, h)
    landmark = pose_predictor(face_image, face_location)
    points = [(p.x, p.y) for p in landmark.parts()]
    # print(points)
    img = face_image
    for p in points:
        img = cv2.circle(img, p, radius=2, color=(0, 0, 255), thickness=-1)
    return img


# %%
faces_folder = r"C:\datasets\face-tests\FaceScrub-faces-10-100-01"
output_folder = r"c:\temp\faces"


def align_faces():
    """生成编码"""
    faces = []
    persons = os.listdir(faces_folder)
    # 按人物目录遍历，生成labelId
    for (pIndex, pName) in enumerate(persons):
        folder = os.path.join(faces_folder, pName)
        imagePaths = paths.list_images(folder)
        for imagePath in imagePaths:
            # print(imagePath)
            face = {"labelId": pIndex, "imagePath": imagePath}
            faces.append(face)

    # 遍历人脸
    for (i, face) in enumerate(faces):
        imagePath = face['imagePath']
        print("[INFO] processing image {}/{}".format(i + 1, len(faces)))
        print(imagePath)
        # load the input image and convert it from RGB (OpenCV ordering) to dlib ordering (RGB)
        image = cv2.imread(imagePath)
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        new_img = align_face(image)
        os.makedirs(output_folder, exist_ok=True)
        target_path = os.path.join(output_folder, f"{i}.jpg")
        cv2.imwrite(target_path, new_img)


start = time.time()
align_faces()
end = time.time()
print(f"align_faces takes {end - start} seconds")
