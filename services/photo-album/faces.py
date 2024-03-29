import cv2
import dlib
import face_recognition
from sklearn.cluster import DBSCAN
from sklearn import neighbors
from psycopg2.extras import Json
import numpy as np
import time

import db
import settings
from logger import get_logger
from utils import rotate_image

bestGuessEps = 0.3

time_detect_faces = 0
time_encode_faces = 0

def reload_faces():
  logger = get_logger()
  logger.info("=========== start reload_faces() ===========")
  conn = db.get_connection()
  try:
    with conn.cursor() as cursor:
      cursor.execute("select id, path from tbl_photo where face_detect_done=false")
      rows = cursor.fetchall()
      logger.info("start to detect&encode faces")
      global time_detect_faces, time_encode_faces
      time_detect_faces = 0
      time_encode_faces = 0
      for (i, row) in enumerate(rows):
        photoId = row[0]
        photoPath = row[1]
        # 人脸检测、编码
        encode_faces(photoId, photoPath, cursor)
        conn.commit()
        logger.info(f"encoding face {i}/{len(rows)}")
      logger.info(f"time_detect_faces: {time_detect_faces} seconds")
      logger.info(f"time_encode_faces: {time_encode_faces} seconds")
      logger.info("end detect&encode faces")
      
      # 自动估算最佳eps值
      logger.info("start to calculate BestEps")
      start = time.time()
      global bestGuessEps
      bestGuessEps = select_cluster_param(cursor)
      end = time.time()
      logger.info(f"calculate BestEps takes {end-start} seconds")
      logger.info(f"DBSCAN param eps value: {bestGuessEps}")

      # 人脸分类
      start = time.time()
      classify_faces(cursor)
      end = time.time()
      logger.info(f"classify_faces takes {end-start} seconds")
      conn.commit()

      # 人脸聚类
      start = time.time()
      cluster_faces(cursor)
      end = time.time()
      logger.info(f"cluster_faces takes {end-start} seconds")
      conn.commit()
  finally:
    db.put_connection(conn)
    logger.info("end reload_faces()")
 

def encode_faces(photoId, photoPath, cursor):
    global time_detect_faces, time_encode_faces
    # load the input image and convert it from RGB (OpenCV ordering)
    # to dlib ordering (RGB)
    image = cv2.imread(photoPath)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 检测人脸
    # detect the (x, y)-coordinates of the bounding boxes
    # corresponding to each face in the input image
    # model can be hog or cnn
    start = time.time()
    MAX_SIZE = 800 # 检测照片的最大尺寸
    h, w = rgb_image.shape[:2]
    ratio = min(MAX_SIZE / h, MAX_SIZE / w)
    if ratio < 1:
        # resize the image
        new_size = (int(w * ratio), int(h * ratio))
        resized_img = cv2.resize(rgb_image, new_size, interpolation=cv2.INTER_AREA)
    else:
      resized_img = rgb_image

    rotation = 0
    boxes = []
    rotateOptions = (0, 90, 180, 270)
    for angle in rotateOptions:
      img = rotate_image(resized_img, angle)
      # 人脸检测
      boxes = face_recognition.face_locations(img, model="hog", number_of_times_to_upsample=1)
      if len(boxes) > 0:
        rotation = angle
        break
    end = time.time()
    time_detect_faces += (end-start)

    # 生成特征
    # compute the facial embedding for the face
    start = time.time()
    encodings = face_recognition.face_encodings(img, known_face_locations=boxes, num_jitters=1)
    end = time.time()
    time_encode_faces += (end-start)

    # delete saved faces of this photo
    cursor.execute("DELETE from tbl_face where photo_id=%s", (photoId,))

    sql = (
      "INSERT INTO tbl_face (photo_id, rotation, location, encoding)"
      " VALUES (%(photoId)s, %(rotation)s, %(box)s, %(encoding)s)"
    )
    for i, (box, enc) in enumerate(zip(boxes, encodings)):
      if ratio < 1:
        origin_box = tuple([int(value / ratio) for value in box])
      else:
        origin_box = box
      cursor.execute(sql, {"photoId": photoId, "rotation": rotation, "box": Json(origin_box), "encoding": Json(enc.tolist())})
    
    # 标记photo已经识别过人脸
    cursor.execute("update tbl_photo set face_detect_done=true where id=%s", (photoId,))


def classify_faces(cursor):
  # 选出所有已有标签的人脸
  logger = get_logger()
  logger.info("========== start classify_faces ==========")
  cursor.execute("select id, encoding, person_id from tbl_face where person_id is not NULL")
  rows = cursor.fetchall()
  labeledFaces = [{"id": row[0], "encoding": row[1], "personId": row[2]} for row in rows]
  if len(rows) < 1:
    return
  
  knownEncodings = [face['encoding'] for face in labeledFaces]
  knownLabels = [face['personId'] for face in labeledFaces]

  # 分类一张人脸（不用了，用方法classify_faces_by_NN代替）
  def classify_one_face(face):
    # 普通的方式找最近的一个
    distances = face_recognition.face_distance(np.array(knownEncodings), np.array(face['encoding']))
    minDist = 1000
    index = -1
    for (i,dist) in enumerate(distances):
      if dist < minDist:
        minDist = dist
        index = i
    # 最相近的人脸
    if minDist < bestGuessEps:
      labelPred = knownLabels[index]
      faceId = face['id']
      logger.info(f"faceID: {faceId}, minDist: {minDist}, predict label: {labelPred}")
      # cursor.execute("update tbl_face set person_id=%s where id=%s", (labelPred, faceId))

  nn = neighbors.NearestNeighbors(n_neighbors=1, n_jobs=-1)
  nn.fit(knownEncodings)
  def classify_faces_by_NN(faces):
    # NN方式找最近的一个
    faceIDs = [face['id'] for face in faces]
    encodings = [face['encoding'] for face in faces]
    # distances和indexes里的每一个元素都是一个数组，数组里只有一个元素（因为n_neighbors=1）
    (distances, indexes) = nn.kneighbors(encodings)
    for (i, distance) in enumerate(distances):
      if distance[0] < bestGuessEps:
        index = indexes[i][0]
        labelPred = knownLabels[index]
        faceId = faceIDs[i]
        logger.info(f"faceID: {faceId}, distance: {distance[0]}, predict label: {labelPred}")
        cursor.execute("update tbl_face set person_id=%s where id=%s", (labelPred, faceId))

  # 选出所有未知人脸
  cursor.execute("select id, encoding from tbl_face where person_id is NULL")
  rows = cursor.fetchall()
  faces = [{"id": row[0], "encoding": row[1]} for row in rows]
  # for face in faces:
  #   classify_one_face(face)
  classify_faces_by_NN(faces)
  logger.info("END classify_faces")

def cluster_faces(cursor):
  "人脸聚类"
  # 只取未知人脸
  logger = get_logger()
  logger.info("========== start cluster_faces ==========")
  cursor.execute("select id, encoding from tbl_face where person_id is NULL")
  rows = cursor.fetchall()
  if len(rows) < 1:
    return

  faces = [{"id": row[0], "encoding": row[1]} for row in rows]
  encodings = [face["encoding"] for face in faces]
  
  # the eps value needs to be chosen carefully
  clt = DBSCAN(metric="euclidean", eps=bestGuessEps, min_samples=5, n_jobs=-1)
  clt.fit(encodings)

  labelIDs = np.unique(clt.labels_)
  # loop over the unique face integers
  for labelID in labelIDs:
    if (labelID < 0):
      # unknown face
      continue

    # 插入新的person
    cursor.execute("INSERT INTO tbl_person (name) VALUES (NULL) RETURNING id;")
    personId = cursor.fetchone()[0]
    logger.info(f"Insert new person {personId}")

    # 当前person的人脸
    idxs = np.where(clt.labels_ == labelID)[0]
    for i in idxs:
      face = faces[i]
      sql = "update tbl_face set person_id=%(personId)s where id=%(id)s;"
      cursor.execute(sql, {"personId": personId, "id": face["id"]})
      logger.info(f"Label face {face['id']} with person {personId}")
  logger.info("END cluster_faces")

def select_cluster_param(cursor):
  "自动选择聚类参数，DBSCAN的eps值"

  MAX_VIOLATE_RATE = 0.05 # 允许5%的照片限制被违反
  DEFAULT_PARAM = 0.3 # 默认值
  MIN_EPS = 0.2 # 最小值 0.2
  MAX_EPS = 0.6 # 最大值 0.6

  # 先获取哪些人脸不应该出现在一个cluster里
  restrictFacesList = get_restrict_faces_list(cursor)
  if len(restrictFacesList) == 0:
    return DEFAULT_PARAM

  # 参数估算是基于所有照片的
  cursor.execute("select id, encoding from tbl_face")
  rows = cursor.fetchall()
  faces = [{"id": row[0], "encoding": row[1]} for row in rows]
  encodings = [face["encoding"] for face in faces]

  # 用于将faceID转成index
  faceDict = {} # {faceID: faceIndex}
  for (i, face) in enumerate(faces):
    faceID = face["id"]
    faceDict[faceID] = i

  bestParamx = DEFAULT_PARAM
  for paramx in np.arange(MIN_EPS, MAX_EPS, 0.01):
    clt = DBSCAN(metric="euclidean", eps=paramx, min_samples=1, n_jobs=-1)
    clt.fit(encodings)
    labels_pred = clt.labels_
    violateRate = check_violate(restrictFacesList, faceDict, labels_pred)
    logger = get_logger()
    logger.info(f"paramx: {round(paramx, 4)}, violateRate: {violateRate}")
    if violateRate < MAX_VIOLATE_RATE:
      bestParamx = paramx
    else:
      return bestParamx

  return bestParamx

def get_restrict_faces_list(cursor):
  "含有2个或以上人脸的照片作为限制条件 [[faceID1,faceID2], [faceID3,faceID4], ...]"
  
  # 选择有2张及以上人脸的照片
  cursor.execute(
    "SELECT photo.id"
    " FROM tbl_photo photo"
    " inner join tbl_face face on photo.id = face.photo_id"
    " group by photo.id"
    " having count(photo.id) > 1"
  )
  rows = cursor.fetchall()
  photoIDs = [row[0] for row in rows]

  # 将照片中的人脸放在数组里
  restrictFacesList = []
  for photoID in photoIDs:
    cursor.execute("select id from tbl_face where photo_id = %s", (photoID, ))
    rows = cursor.fetchall()
    faceIDs = [row[0] for row in rows]
    restrictFacesList.append(faceIDs)

  return restrictFacesList


def check_violate(restrictFacesList, faceDict, labels_pred):
    "计算限制条件被违反的照片个数（比例）"
    violateCount = 0
    for restrictFaces in restrictFacesList:
        # restrictFaces是一张照片中出现的人脸列表，它们不应该出现在同一个cluster里
        personLabelSet = set()
        for faceID in restrictFaces:
            faceIndex = faceDict[faceID]
            label = labels_pred[faceIndex]
            personLabelSet.add(label)
        if len(personLabelSet) < len(restrictFaces):
            # 类簇个数少于人脸数，说明有的人脸被聚在了一个cluster里
            violateCount += 1

    violateRate = round(float(violateCount) / len(restrictFacesList), 4)
    logger = get_logger()
    logger.info(f'违反限制{violateCount}/{len(restrictFacesList)} = {violateRate}')
    return violateRate
