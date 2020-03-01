import cv2
import face_recognition
from sklearn.cluster import DBSCAN
from psycopg2.extras import Json
import numpy as np

import db
import settings
from logger import get_logger

bestGuessEps = 0.3

def reload_faces():
  logger = get_logger()
  conn = db.get_connection()
  try:
    with conn.cursor() as cursor:
      cursor.execute("select id, path from tbl_photo where face_detect_done=false")
      rows = cursor.fetchall()
      for (i, row) in enumerate(rows):
        photoId = row[0]
        photoPath = row[1]
        # 人脸检测、编码
        encode_faces(photoId, photoPath, cursor)
        conn.commit()
        logger.info(f"encoding face {i}/{len(rows)}")
      
      # 自动估算最佳eps值
      global bestGuessEps
      bestGuessEps = select_cluster_param(cursor)
      logger = get_logger()
      logger.info(f"DBSCAN param eps value: {bestGuessEps}")

      # 人脸分类
      classify_faces(cursor)
      conn.commit()

      # 人脸聚类
      cluster_faces(cursor)
      conn.commit()
  finally:
    db.put_connection(conn)
 

def encode_faces(photoId, photoPath, cursor):
    # load the input image and convert it from RGB (OpenCV ordering)
    # to dlib ordering (RGB)
    image = cv2.imread(photoPath)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 检测人脸
    # detect the (x, y)-coordinates of the bounding boxes
    # corresponding to each face in the input image
    # model can be hog or cnn
    boxes = face_recognition.face_locations(rgb, model="hog")
          
    # 生成特征
    # compute the facial embedding for the face
    encodings = face_recognition.face_encodings(rgb, known_face_locations=boxes, num_jitters=1)

    # delete saved faces of this photo
    cursor.execute("DELETE from tbl_face where photo_id=%s", (photoId,))

    sql = (
      "INSERT INTO tbl_face (photo_id, location, encoding)"
      " VALUES (%(photoId)s, %(box)s, %(encoding)s)"
    )
    for i, (box, enc) in enumerate(zip(boxes, encodings)):
      cursor.execute(sql, {"photoId": photoId, "box": Json(box), "encoding": Json(enc.tolist())})
    
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

  # 分类一张人脸
  def classify_one_face(face):
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
      cursor.execute("update tbl_face set person_id=%s where id=%s", (labelPred, faceId))

  # 选出所有未知人脸
  cursor.execute("select id, encoding from tbl_face where person_id is NULL")
  rows = cursor.fetchall()
  faces = [{"id": row[0], "encoding": row[1]} for row in rows]
  for face in faces:
    classify_one_face(face)
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

  MAX_VIOLATE_RATE = 0.15 # 允许15%的照片限制被违反
  DEFAULT_PARAM = 0.3 # 默认值

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
  for paramx in np.arange(0.2, 0.6, 0.01):
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
