import os
import logging
from imutils import paths

from db import get_db_connection
import settings


def reload_photos():
  imagePaths = paths.list_images(settings.USER_PHOTO_HOME)
  logger = logging.getLogger("logger")
  conn = get_db_connection()

  sql = (
    "INSERT INTO tbl_photo (path, last_updated)"
    " VALUES (%(path)s, NOW())"
    " ON CONFLICT (path) DO UPDATE"
    " SET last_updated = NOW()"
    ";"
  )

  with conn.cursor() as cursor:
    for imagePath in imagePaths:
      logger.info(imagePath)
      cursor.execute(sql, {"path": imagePath})
    conn.commit()
