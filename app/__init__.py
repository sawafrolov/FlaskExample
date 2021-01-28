from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_babel import Babel, lazy_gettext as _l
from flask_moment import Moment
from flask_mail import Mail
from googletrans import Translator
from app.elasticsearch import enable_elasticsearch
import logging
from logging.handlers import RotatingFileHandler


db = SQLAlchemy()
login = LoginManager()
login.login_view = "auth.login"
login.login_message = _l("Please log in to access this page.")
bootstrap = Bootstrap()
babel = Babel()
translator = Translator()
moment = Moment()
mail = Mail()


def create_app(config_file="config"):

    app = Flask(__name__)
    app.config.from_object(config_file)
    db.init_app(app)
    login.init_app(app)
    bootstrap.init_app(app)
    babel.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    app.elasticsearch = enable_elasticsearch(app.config["ELASTICSEARCH_URL"])

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    if not app.debug:
        file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info("microblog startup")

    return app


@babel.localeselector
def get_locale():
    return "ru"
