import os
import logging
from imutils import paths

import db
import settings


def reload_photos():
  imagePaths = paths.list_images(settings.USER_PHOTO_HOME)
  logger = logging.getLogger("logger")
  conn = db.get_connection()

  sql = (
    "INSERT INTO tbl_photo (path, last_updated)"
    " VALUES (%(path)s, NOW())"
    " ON CONFLICT (path) DO UPDATE"
    " SET last_updated = NOW()"
    ";"
  )

  try:
    with conn.cursor() as cursor:
      for imagePath in imagePaths:
        logger.info(imagePath)
        cursor.execute(sql, {"path": imagePath})
      conn.commit()
  finally:
    db.put_connection(conn)


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
    sql = f"SELECT (id) from tbl_photo LIMIT {limit} OFFSET {offset}"
    with conn.cursor() as cursor:
      cursor.execute(sql)
      rows = cursor.fetchall() 
      return [{"id": row[0]} for row in rows]
  finally:
    db.put_connection(conn)


def get_photo_path(id):
  conn = db.get_connection()
  try:
    sql = "SELECT (path) from tbl_photo where id=%(id)s"
    with conn.cursor() as cursor:
      cursor.execute(sql, {"id": id})
      row = cursor.fetchone()
      if row is None:
        return None
      else:
        return row[0]
  finally:
    db.put_connection(conn)
    