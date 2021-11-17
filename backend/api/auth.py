from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash
from os import environ 
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    print(f'Checking username: {username}')
    if username == environ['USER'] \
        and check_password_hash(generate_password_hash(environ['PASSWORD']), password):
        return username