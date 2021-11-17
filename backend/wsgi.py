
from api.main import app 
from api.app import app

import os
if __name__ == "__main__":
        app.run(port=os.environ['PORT'])