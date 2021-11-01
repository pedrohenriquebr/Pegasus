from flask import Flask
from dotenv import load_dotenv
app = Flask(__name__)
 
@app.route("/")
def home_view():
        return "<h1>Hello world</h1>"