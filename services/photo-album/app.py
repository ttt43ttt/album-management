from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
import random
import string
import json
import logging

from logger import create_logger
from photos import reload_photos

app = Flask(__name__)


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
    return {}

if __name__ == '__main__':
    create_logger("log.txt")
    logger = logging.getLogger("logger")
    logger.info("service starts...")

    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=10080)