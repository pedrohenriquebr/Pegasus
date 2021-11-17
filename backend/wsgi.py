
from api.main import app as application
# from api.app import app

app = application
import os
if __name__ == "__main__":
        app.run(port=os.environ['PORT'])