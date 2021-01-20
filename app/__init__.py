from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_babel import Babel, lazy_gettext as _l
from flask_moment import Moment
from flask_mail import Mail
from googletrans import Translator
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)
login = LoginManager()
login.init_app(app)
login.login_view = "auth.login"
login.login_message = _l("Please log in to access this page.")
bootstrap = Bootstrap(app)
babel = Babel(app)
translator = Translator()
moment = Moment(app)
mail = Mail(app)

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix="/auth")

from app.main import bp as main_bp
app.register_blueprint(main_bp, url_prefix="/main")

@babel.localeselector
def get_locale():
    return "en"


if not app.debug:
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("microblog startup")
