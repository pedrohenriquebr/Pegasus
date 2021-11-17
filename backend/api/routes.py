from flask import Blueprint, flash, request, redirect, url_for,send_from_directory,jsonify,request
from werkzeug.utils import secure_filename
import os
from api import config
from api.services import TransactionsService 
from api.db_connection import Connection 
from flask_cors import CORS, cross_origin
from api.auth import auth

transactions_service = TransactionsService(Connection.get_connection())


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
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # pegasus.import_statement(os.path.join(app.config['UPLOAD_FOLDER'], filename),'inter',request.form.get('id_account',type=int))
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

## TRANSACTIONS

transactions_page = Blueprint('transactions', __name__)

@transactions_page.route('/search')
@cross_origin()
@auth.login_required
def search_transactions():
    return jsonify(transactions_service.search_transactions(request.args.get('offset',0,int), request.args.get('limit',10,int)))

@transactions_page.route('/get-all',methods=['POST'])
@cross_origin()
@auth.login_required
def get_all_transactions():
    d = request.get_json(force=True)
    page  = d.get('page',0)
    limit = d.get('limit',10)
    id_account = d.get('id_account',1)
    print(transactions_service.repo.find(lambda x: x.ID_Account == 1)[0].DS_Description)
    
    return jsonify(transactions_service.get_all_transactions(id_account, page, limit))
    