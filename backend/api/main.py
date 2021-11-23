from api.auth import auth
from api.app import app

import os
from flask import send_from_directory

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@auth.login_required
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')
if __name__ == '__main__':
    app.run(debug=True)