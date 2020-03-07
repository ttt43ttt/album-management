from flask import Flask, send_file, request, redirect, jsonify, url_for, make_response
import random
import string
import json
import logging

from logger import create_logger
from watch_folder import start_watch_files
from photos import reload_photos, list_photos, get_photo_path, count_photos
from faces import reload_faces
from persons import list_persons, get_person_image, list_person_photos, count_person_photos,\
rename_person, merge_persons, remove_persons, link_photos_to_person, create_person

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

@app.route('/api/faces/reload', methods=['POST'])
def reloadFaces():
    "Reload faces from photos"
    reload_faces()
    return {"data": "OK"}

@app.route('/api/photos/list', methods=['POST'])
def listPhotos():
    query = request.json
    pageNumber = query["pageNumber"]
    pageSize = query["pageSize"]
    skipCount = pageSize*(pageNumber-1)
    total = count_photos()
    meta = {"total": total, "limit": pageSize, "skip": skipCount}
    
    photos = list_photos(pageSize, skipCount)
    data = []
    for photo in photos:
        id = photo["id"]
        digest = photo["digest"]
        url = f"/api/photos/{id}/content?d={digest}"
        data.append({"id": id, "url": url})
    return {"data": data, "meta": meta}

@app.route('/api/photos/<id>/content', methods=['GET'])
def showPhotoContent(id):
    imgPath = get_photo_path(id)
    if imgPath is None:
        return make_response("", 404)
    try:
        return send_file(imgPath)
    except Exception as e:
        logger.warning(e)
        return make_response("", 404)

@app.route('/api/persons/list', methods=['POST'])
def listPersons():
    persons = list_persons()
    for person in persons:
        id = person["id"]
        person["url"] = f"/api/persons/{id}/image"
    return {"data": persons}

@app.route('/api/persons/<id>/rename', methods=['POST'])
def renamePerson(id):
    query = request.json
    name = query["name"]
    rename_person(id, name)
    return {"data": "OK"}

@app.route('/api/persons/merge', methods=['POST'])
def mergePersons():
    query = request.json
    ids = query["ids"]
    merge_persons(ids)
    return {"data": "OK"}

@app.route('/api/persons/remove', methods=['POST'])
def removePersons():
    query = request.json
    ids = query["ids"]
    remove_persons(ids)
    return {"data": "OK"}

@app.route('/api/persons/<id>/image', methods=['GET'])
def showPersonImage(id):
    imgPath = get_person_image(id)
    if imgPath is None:
        return make_response("", 404)
    return send_file(imgPath)

@app.route('/api/persons/<id>/photos/list', methods=['POST'])
def listPersonPhotos(id):
    query = request.json
    pageNumber = query["pageNumber"]
    pageSize = query["pageSize"]
    skipCount = pageSize*(pageNumber-1)
    total = count_person_photos(id)
    meta = {"total": total, "limit": pageSize, "skip": skipCount}
    
    photos = list_person_photos(id, pageSize, skipCount)
    data = []
    for photo in photos:
        id = photo["id"]
        digest = photo["digest"]
        url = f"/api/photos/{id}/content?d={digest}"
        data.append({"id": id, "url": url})
    return {"data": data, "meta": meta}

@app.route('/api/persons/link-photos', methods=['POST'])
def linkPhotosToPerson():
    query = request.json
    photoIds = query["photoIds"]
    personId = query["personId"]
    newPersonId = query.get("newPersonId")
    newPersonName = query.get("newPersonName")
    if not personId:
        return make_response("personId是必须的", 400)
    if newPersonName:
        newPersonId = create_person(newPersonName)
    if newPersonId is None:
        newPersonId = -1
    link_photos_to_person(photoIds, personId, newPersonId)
    return {"data": "OK"}

if __name__ == '__main__':
    logger.info("service starts...")
    reload_photos()
    start_watch_files()

    app.secret_key = 'super_secret_key'
    app.debug = True
    logger.info("listening on port 10080")
    app.run(host='0.0.0.0', port=10080)