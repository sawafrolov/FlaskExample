from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)
login = LoginManager()
login.init_app(app)
login.login_view = "login"
