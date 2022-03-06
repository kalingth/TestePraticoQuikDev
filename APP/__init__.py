from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_object('config')
db = SQLAlchemy(app)
ma = Marshmallow(app)

from .Models import users, posts, comments
from .routes import routes

