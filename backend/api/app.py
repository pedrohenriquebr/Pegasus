from os import environ
from flask import Flask
from flask_cors import CORS
from api import config
import api.routes as routes
from werkzeug.security import generate_password_hash


def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
    app.config['USER'] = environ.get('USER')
    app.config['PASSWORD'] = generate_password_hash(environ.get('PASSWORD'))
    cors = CORS(app)
    app.register_blueprint(routes.transactions_page,url_prefix='/api/transactions')
    print(app.url_map)
    return app

app = create_app()