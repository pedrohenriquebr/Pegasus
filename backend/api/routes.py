from flask import Blueprint, flash, request, redirect, url_for,send_from_directory,jsonify,request
from werkzeug.utils import secure_filename
import os
from api import config
from api.services import TransactionsService,AccountsService,CategoriesService,ExportationService
from api.db_connection import Connection 
from flask_cors import CORS, cross_origin
from api.auth import auth
from api.uof import Uof 
from api.caching import cache

_uof  = Uof(Connection.get_connection())
transactions_service = TransactionsService(_uof)
accounts_service  = AccountsService(_uof)
categories_service  = CategoriesService(_uof)
exportation_service = ExportationService(_uof)
# importation_service = ImportationService(_uof)

def download_file(name):
    return send_from_directory(os.path.abspath(config.UPLOAD_FOLDER), name)
 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


## TRANSACTIONS

transactions_page = Blueprint('transactions', __name__)

@transactions_page.route('/get-all',methods=['POST'])
@cache.cached(timeout=3)
@cross_origin()
@auth.login_required
def get_all_transactions_by_account():
    d = request.get_json(force=True)
    page  = int(d.get('page',0))
    limit = int(d.get('limit',10))
    id_account = int(d.get('id_account',1))
    
    return jsonify(transactions_service.get_all_transactions(id_account, page, limit))



## ACCOUNTS

accounts_page = Blueprint('accounts', __name__)

@accounts_page.route('/get-all',)
@cache.cached(timeout=3)
@cross_origin()
@auth.login_required
def search_all_accounts():
    d = request.get_json(force=True)
    page  = int(d.get('page',0))
    limit = int(d.get('limit',100))
    
    return jsonify(accounts_service.get_all_accounts(page, limit))


@accounts_page.route('/autocomplete')
@cache.cached(timeout=3)
@cross_origin()
@auth.login_required
def autcomplete_accounts():
    return jsonify(accounts_service.get_all_accounts_names())

categories_page  = Blueprint('categories', __name__)

@categories_page.route('/autocomplete',)
@cache.cached(timeout=3)
@cross_origin()
@auth.login_required
def autcomplete_categories():
    return jsonify(categories_service.get_all_categories_names())




## EXPORTATION

exportation_page = Blueprint('exportation', __name__)

@exportation_page.route('/download', methods=['GET'])
@cross_origin()
@auth.login_required
def download_exportation():
    id_account = int(request.args.get('id_account',0))
    return download_file(exportation_service.export_data(id_account))


@exportation_page.route('/upload', methods=['POST'])
@cross_origin()
@auth.login_required
def upload_file():

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
        file.save(os.path.join(config.UPLOAD_FOLDER, filename))
        try:
            rs  = exportation_service.import_statement(os.path.join(config.UPLOAD_FOLDER, filename),request.form.get('bank',type=str),request.form.get('id_account',type=int))
            if rs is not None:
                return jsonify({'status':'warning','message':'There are some records without category', 'data':rs})
        except Exception as e:
            return jsonify({"status":"error", "error": str(e)})
        
        return jsonify({"status": "success"})
    else:
        ## send error status
        return jsonify({"status": "error", "error": "File not allowed"})
