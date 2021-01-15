from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_babel import Babel, lazy_gettext as _l
from flask_moment import Moment
from flask_mail import Mail
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)
login = LoginManager()
login.login_view = "login"
login.login_message = _l("Please log in to access this page.")
bootstrap = Bootstrap(app)
babel = Babel(app)
moment = Moment(app)
mail = Mail(app)


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config["LANGUAGES"])


if not app.debug:
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("microblog startup")
