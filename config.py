import os
import email_config


DEFAULT_LANGUAGE = "en"
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = "you-shall-not-pass"
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False
POSTS_PER_PAGE = 10
ELASTICSEARCH_URL = "http://localhost:9200"
MAIL_SERVER = email_config.MAIL_SERVER
MAIL_PORT = email_config.MAIL_PORT
MAIL_USE_TLS = email_config.MAIL_USE_TLS
MAIL_USERNAME = email_config.MAIL_USERNAME
MAIL_PASSWORD = email_config.MAIL_PASSWORD
ADMINS = ['sawa.frolov@yandex.ru']
