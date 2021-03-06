import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import cv2
import tensorflow as tf
import numpy as np
from os.path import join, dirname, realpath
from paraUsarApi import reconoceLaCamiseta

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'Prueba')
#UPLOAD_FOLDER = './Prueba'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            to = "/reconoce/"+filename
            print(to)
            return redirect(to)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method="post" enctype="multipart/form-data">
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/prueba/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/reconoce/<path>')
def reconocimiento(path):
    path=UPLOAD_FOLDER+"/"+path
    print(path)
    return reconoceLaCamiseta(path)

app.run("0.0.0.0", 5000, debug=False, threaded=False)

#reconoceLaCamiseta('Prueba/20c6d52136.jpg')