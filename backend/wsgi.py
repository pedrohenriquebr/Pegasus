
from api.auth import auth
from api.app import app

@app.route('/')
@auth.login_required
def index():
    return "Hello, %s!" % auth.username()
if __name__ == "__main__":
        app.run()