import os
from imutils import paths
from PIL import Image # pip install Pillow
import hashlib
import time

import db
import settings
from logger import get_logger


def reload_photos():
  imagePaths = paths.list_images(settings.USER_PHOTO_HOME)
  logger = get_logger()
  conn = db.get_connection()
  try:
    with conn.cursor() as cursor:
      for imagePath in imagePaths:
        # 检查文件path是否存在表中
        cursor.execute("select id, digest from tbl_photo where path=%s", (imagePath,))
        row = cursor.fetchone()
        if row is None:
          # 文件path不存在，直接插入
          digest = get_file_digest(imagePath)
          takenTime = get_image_taken_time(imagePath)
          sql = (
            "INSERT INTO tbl_photo (path, digest, taken_time, last_scanned)"
            " VALUES (%(path)s, %(digest)s, TIMESTAMP %(takenTime)s, NOW())"
          )
          cursor.execute(sql, {"path": imagePath, "digest": digest, "takenTime": takenTime})
        else:
          # 如果文件path已经在表中，检查文件digest是否一致
          id = row[0]
          oldDigest = row[1]
          newDigest = get_file_digest(imagePath)
          if newDigest == oldDigest:
            # digest一致，只更新last_scanned
            cursor.execute("update tbl_photo set last_scanned=NOW()")
          else:
            # digest不一致，删除老的photo及关联的face
            cursor.execute("delete from tbl_face where photo_id=%s", (id,))
            cursor.execute("delete from tbl_photo where id=%s", (id,))
            # 插入新的行
            takenTime = get_image_taken_time(imagePath)
            sql = (
              "INSERT INTO tbl_photo (path, digest, taken_time, last_scanned)"
              " VALUES (%(path)s, %(digest)s, TIMESTAMP %(takenTime)s, NOW())"
            )
            cursor.execute(sql, {"path": imagePath, "digest": newDigest, "takenTime": takenTime})
        # logger.info(imagePath)
        conn.commit()
  finally:
    db.put_connection(conn)


def get_image_taken_time(path) -> str:
  "获取图片拍摄时间或修改时间"
  exif = Image.open(path)._getexif()
  # 拍摄时间
  takenTime = exif.get(36867) if exif else None
  if takenTime:
    try:
      t = time.strptime(takenTime, "%Y:%m:%d %H:%M:%S")
      takenTime = time.strftime("%Y-%m-%d %H:%M:%S", t)
      return takenTime
    except Exception:
      takenTime = None
  # 文件修改时间
  mtime = os.path.getmtime(path)
  t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mtime))
  return t

def get_file_digest(path) -> str:
  # lets read stuff in 1MB chunks
  BUF_SIZE = 1*1024*1024
  sha1 = hashlib.sha1()
  with open(path, 'rb') as f:
      while True:
          data = f.read(BUF_SIZE)
          if not data:
              break
          sha1.update(data)
  return sha1.hexdigest()

def count_photos():
  conn = db.get_connection()
  try:
      with conn.cursor() as cursor:
        cursor.execute("SELECT count(id) from tbl_photo")
        row = cursor.fetchone()
        return row[0]
  finally:
    db.put_connection(conn)


def list_photos(limit = 20, offset = 0):
  conn = db.get_connection()
  try:
    sql = f"SELECT id from tbl_photo order by taken_time desc LIMIT {limit} OFFSET {offset}"
    with conn.cursor() as cursor:
      cursor.execute(sql)
      rows = cursor.fetchall() 
      return [{"id": row[0]} for row in rows]
  finally:
    db.put_connection(conn)


def get_photo_path(id):
  conn = db.get_connection()
  try:
    sql = "SELECT path from tbl_photo where id=%(id)s"
    with conn.cursor() as cursor:
      cursor.execute(sql, {"id": id})
      row = cursor.fetchone()
      if row is None:
        return None
      else:
        return row[0]
  finally:
    db.put_connection(conn)
