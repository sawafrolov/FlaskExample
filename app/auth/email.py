from flask import render_template, current_app
from flask_babel import _
from app.email import send_email
from app.tokens import get_reset_password_token


def send_password_reset_email(user):
    token = get_reset_password_token(user)
    send_email(
        _("[Microblog] Reset Your Password"),
        sender=current_app.config["ADMINS"][0],
        recipients=[user.email],
        text_body=render_template("email/reset_password.txt", user=user, token=token),
        html_body=render_template("email/reset_password.html", user=user, token=token)
    )
