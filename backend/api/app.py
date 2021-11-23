from os import environ
from flask import Flask
from flask_cors import CORS
from api import config
import api.routes as routes
from api.caching import cache
from werkzeug.security import generate_password_hash


def create_app():
    app = Flask(__name__,static_folder='../build',static_url_path='/')
    cache.init_app(app)
    app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
    app.config['USER'] = environ.get('USER')
    app.config['PASSWORD'] = generate_password_hash(environ.get('PASSWORD'))
    cors = CORS(app)
    app.register_blueprint(routes.transactions_page,url_prefix='/api/transactions')
    app.register_blueprint(routes.accounts_page,url_prefix='/api/accounts')
    app.register_blueprint(routes.categories_page,url_prefix='/api/categories')
    app.register_blueprint(routes.exportation_page,url_prefix='/api/export')
    print(app.url_map)
    return app

app = create_app()