from flask import Flask,g

from dotenv import load_dotenv

from api import config

import api.routes as routes


def create_app() -> Flask:
    load_dotenv()
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
    ## prefix api/v1

    app.add_url_rule('/api/upload', view_func=routes.upload_file)
    app.add_url_rule('/api/uploads/<name>', view_func=routes.download_file)

    ## TRANSACTIONS
    # app.add_url_rule('/api/transactions', methods=['POST','GET'],view_func=routes.search_transactions)
    # app.add_url_rule('/api/transactions/get-all', methods=['POST'],view_func=routes.get_all_transactions)
    app.register_blueprint(routes.transactions_page,url_prefix='/api/transactions')

    print(app.url_map)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)