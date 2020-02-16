import cv2
import logging
import face_recognition
from sklearn.cluster import DBSCAN
from psycopg2.extras import Json
import numpy as np

import db
import settings

def reload_faces():
  conn = db.get_connection()
  try:
    with conn.cursor() as cursor:
      cursor.execute("select id, path from tbl_photo")
      rows = cursor.fetchall()
      for row in rows:
        photoId = row[0]
        photoPath = row[1]
        # 人脸检测、编码
        encode_face(photoId, photoPath, cursor)
        conn.commit()
      
      # 人脸分类、聚类
      cluster_face(cursor)
      conn.commit()
  finally:
    db.put_connection(conn)
 

def encode_face(photoId, photoPath, cursor):
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
      "INSERT INTO tbl_face (photo_id, location, embedding)"
      " VALUES (%(photoId)s, %(box)s, %(embedding)s)"
    )
    for i, (box, enc) in enumerate(zip(boxes, encodings)):
      cursor.execute(sql, {"photoId": photoId, "box": Json(box), "embedding": Json(enc.tolist())})


def cluster_face(cursor):
  "人脸聚类"
  # 只取未知人脸
  cursor.execute("select id, location, embedding from tbl_face where person_id is NULL")
  rows = cursor.fetchall()
  faces = [{"id": row[0], "location": row[1], "encoding": row[2]} for row in rows]
  encodings = [face["encoding"] for face in faces]
  
  # the eps value needs to be chosen carefully
  clt = DBSCAN(metric="euclidean", eps=0.4, min_samples=5, n_jobs=-1)
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

    # 当前person的人脸
    idxs = np.where(clt.labels_ == labelID)[0]
    for i in idxs:
      face = faces[i]
      sql = "update tbl_face set person_id=%(personId)s where id=%(id)s;"
      cursor.execute(sql, {"personId": personId, "id": face["id"]})
