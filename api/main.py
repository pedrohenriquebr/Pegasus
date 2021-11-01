from flask import Flask
from dotenv import load_dotenv
app = Flask(__name__)
 
@app.route("/")
def home_view():
        return "<h1>Hello opa</h1>"

if __name__ == "__main__":
  app.run()