from flask import render_template, current_app
from flask_babel import _
from jwt import decode, encode
from time import time
from app.email import send_email
from app.select_dao import select_user_by_id


def get_reset_password_token(user, expires_in=600):
    return encode(
        {
            'reset_password': user.id,
            'exp': time() + expires_in
        },
        current_app.config["SECRET_KEY"],
        algorithm='HS256'
    )


def send_password_reset_email(user):
    token = get_reset_password_token(user)
    send_email(
        _("[Microblog] Reset Your Password"),
        sender=current_app.config["ADMINS"][0],
        recipients=[user.email],
        text_body=render_template("email/reset_password.txt", user=user, token=token),
        html_body=render_template("email/reset_password.html", user=user, token=token)
    )


def verify_reset_password_token(token):
    try:
        user_id = decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=['HS256']
        )['reset_password']
    except:
        return
    return select_user_by_id(user_id)
