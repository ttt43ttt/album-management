import cv2
import face_recognition
from psycopg2.extras import Json

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

        # commit to DB
        conn.commit()
  # 聚类
  finally:
    db.put_connection(conn)
 

def detect_face():
  pass