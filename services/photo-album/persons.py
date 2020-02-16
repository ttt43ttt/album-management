import os
import cv2

import db
import settings
from logger import get_logger

def list_persons():
  conn = db.get_connection()
  try:
    sql = (
      "select person.id, person.name, count(photo.id)"
      " from tbl_person person"
      " inner join tbl_face face on person.id = face.person_id"
      " inner join tbl_photo photo on face.photo_id = photo.id"
      " group by person.id"
    )
    with conn.cursor() as cursor:
      cursor.execute(sql)
      rows = cursor.fetchall() 
      return [{"id": row[0], "name": row[1], "photoCount": row[2]} for row in rows]
  finally:
    db.put_connection(conn)


def get_person_image(personId):
  "生成并返回人物图像的filepath"
  conn = db.get_connection()
  try:
    sql = (
      "select face.id faceId, photo.path, face.location"
      " from tbl_face face"
      " inner join tbl_photo photo on face.photo_id = photo.id"
      " where face.person_id = %s"
      " limit 1"
    )
    with conn.cursor() as cursor:
      cursor.execute(sql, (personId,))
      row = cursor.fetchone()
      if row is None:
        return None
      faceId = row[0]
      photoPath = row[1]
      faceBox = row[2]
      # 截取人脸
      image = cv2.imread(photoPath)
      (top, right, bottom, left) = faceBox
      faceImage = image[top:bottom, left:right]
      # 保存到磁盘
      os.makedirs(settings.PERSON_IMAGES_HOME, exist_ok=True)
      path = os.path.join(settings.PERSON_IMAGES_HOME, f"{faceId}.jpg")
      cv2.imwrite(path, faceImage)
      return path
  finally:
    db.put_connection(conn)


def list_person_photos(personId, limit=20, offset=0):
  "返回包含某个人物的照片列表"
  conn = db.get_connection()
  try:
    sql = (
      "select photo.id"
      " from tbl_photo photo"
      " inner join tbl_face face on photo.id = face.photo_id"
      " where face.person_id = %s"
      " LIMIT %s OFFSET %s"
    )
    with conn.cursor() as cursor:
      cursor.execute(sql, (personId, limit, offset))
      rows = cursor.fetchall()
      return [{"id": row[0]} for row in rows]
  finally:
    db.put_connection(conn)


def count_person_photos(personId):
  "返回包含某个人物的照片总数"
  conn = db.get_connection()
  try:
    sql = (
      "select count(photo.id)"
      " from tbl_photo photo"
      " inner join tbl_face face on photo.id = face.photo_id"
      " where face.person_id = %s"
    )
    with conn.cursor() as cursor:
      cursor.execute(sql, (personId,))
      row = cursor.fetchone()
      return row[0]
  finally:
    db.put_connection(conn)


def rename_person(personId, name):
  conn = db.get_connection()
  try:
    with conn.cursor() as cursor:
      cursor.execute("update tbl_person set name=%s where id=%s", (name, personId))
    conn.commit()
  finally:
    db.put_connection(conn)


def merge_persons(ids):
  conn = db.get_connection()
  try:
    with conn.cursor() as cursor:
      newId = ids[0]
      idsToRemove = tuple(ids[1:])
      cursor.execute("update tbl_face set person_id=%s where person_id in %s", (newId, idsToRemove))
      cursor.execute("delete from tbl_person where id in %s", (idsToRemove,))
    conn.commit()
  finally:
    db.put_connection(conn)


def remove_persons(ids):
  conn = db.get_connection()
  try:
    with conn.cursor() as cursor:
      idsToRemove = tuple(ids)
      cursor.execute("update tbl_face set person_id=NULL where person_id in %s", (idsToRemove,))
      cursor.execute("delete from tbl_person where id in %s", (idsToRemove,))
    conn.commit()
  finally:
    db.put_connection(conn)
