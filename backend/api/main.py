from flask import Flask

from dotenv import load_dotenv

from api import config

import api.routes as routes
import db_connection


def create_app() -> Flask:
    load_dotenv()
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
    ## prefix api/v1

    app.add_url_rule('/api/upload', view_func=routes.upload_file)
    app.add_url_rule('/api/uploads/<name>', view_func=routes.download_file)
    app.add_url_rule('/api/transactions', methods=['POST','GET'],view_func=routes.search_transactions)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)