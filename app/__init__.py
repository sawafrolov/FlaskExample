from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_openid import OpenID
import os
from config import basedir

app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)
login = LoginManager()
login.init_app(app)
login.login_view = "login"
oid = OpenID(app, os.path.join(basedir, "tmp"))
