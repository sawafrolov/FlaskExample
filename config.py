import os
import email_config

LANGUAGES = ['en', 'ru']
basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False
POSTS_PER_PAGE = 10
MAIL_SERVER = email_config.MAIL_SERVER
MAIL_PORT = email_config.MAIL_PORT
MAIL_USE_TLS = email_config.MAIL_USE_TLS
MAIL_USERNAME = email_config.MAIL_USERNAME
MAIL_PASSWORD = email_config.MAIL_PASSWORD
ADMINS = ['sawa.frolov@yandex.ru']
