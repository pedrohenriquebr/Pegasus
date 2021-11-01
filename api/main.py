from flask import Flask, flash, request, redirect, url_for
from flask import send_from_directory
from dotenv import load_dotenv
import database.dbconnection as dbconnection
import  database.schema as schema
from pegasus2 import Pegasus
import os
import sys


from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'temp'
ALLOWED_EXTENSIONS = {'csv'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

load_dotenv()

db = dbconnection.DbConnection()
db.connect()

pegasus  = Pegasus(db, debug=True,)
pegasus.load_data()

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(os.path.abspath(app.config["UPLOAD_FOLDER"]), name)
 
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
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            pegasus.import_statement(os.path.join(app.config['UPLOAD_FOLDER'], filename),'inter')
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
if __name__ == "__main__":
  app.run()