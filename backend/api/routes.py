from flask import flash, request, redirect, url_for,send_from_directory,jsonify,request
from werkzeug.utils import secure_filename
import os
from api import config
from services import TransactionsService 
from db_connection import db


transactions_service = TransactionsService(db)

def download_file(name):
    return send_from_directory(os.path.abspath(config.UPLOAD_FOLDER), name)
 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            pegasus.import_statement(os.path.join(app.config['UPLOAD_FOLDER'], filename),'inter',request.form.get('id_account',type=int))
            # return 200 request
            return jsonify({"status": "success"})
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

def search_transactions():
    return jsonify(transactions_service.search_transactions(10))
    