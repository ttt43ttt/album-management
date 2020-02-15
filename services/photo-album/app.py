from flask import Flask, send_file, request, redirect, jsonify, url_for, make_response
import random
import string
import json
import logging

from logger import create_logger
from photos import reload_photos, list_photos, get_photo_path, count_photos

app = Flask(__name__)

create_logger("log.txt")
logger = logging.getLogger("logger")


@app.route('/')
def showHello():
    return "Hello"


@app.route('/api/photos/reload', methods=['POST'])
def reloadPhotos():
    "Reload photos from disk"
    reload_photos()
    return {"data": "OK"}

@app.route('/api/photos/list', methods=['POST'])
def listPhotos():
    query = request.json
    pageNumber = query["pageNumber"]
    pageSize = query["pageSize"]
    skipCount = pageSize*(pageNumber-1)
    total = count_photos()
    photos = list_photos(pageSize, skipCount)
    meta = {"total": total, "limit": pageSize, "skip": skipCount}
    return {"data": photos, "meta": meta}


@app.route('/api/photos/<id>', methods=['GET'])
def showPhoto(id):
    imgPath = get_photo_path(id)
    if imgPath is None:
        return make_response("", 404)
    return send_file(imgPath)

if __name__ == '__main__':
    logger.info("service starts...")
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=10080)