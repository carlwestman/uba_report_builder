from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

import config

## When in Dev environment copy config to dev_config
## in order to not risk adding secrets to git
# import dev_config

db = SQLAlchemy(app)

from routes import *

if __name__ == '__main__':
    app.run(debug=True)
