import os

MAIL_SERVER = "smtp.googlemail.com"
MAIL_PORT = 587
MAIL_USE_TLS = 1
MAIL_USERNAME = os.environ.get("GMAIL_USERNAME") or ""
MAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD") or ""
