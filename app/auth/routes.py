from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user
from flask_babel import _
from app import login
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.dao import create_user, change_password
from app.select_dao import select_user_by_id, select_user_by_username, select_user_by_email
from app.auth.reset_password import send_password_reset_email, verify_reset_password_token


@login.user_loader
def load_user(id):
    return select_user_by_id(id)


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        create_user(form.username.data, form.password.data, form.email.data)
        flash(_("Congratulations, you are now a registered user!"))
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", title=_("Register"), form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = select_user_by_username(form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash(_("Invalid username or password"))
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        return redirect(next_page or url_for("main.index"))
    return render_template("auth/login.html", title=_("Sign In"), form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@bp.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = select_user_by_email(form.email.data)
        if user:
            send_password_reset_email(user)
        flash(_("Check your email for the instructions to reset your password"))
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password_request.html", title=_("Reset Password"), form=form)


@bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    user = verify_reset_password_token(token)
    if not user:
        return redirect(url_for("main.index"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        change_password(user, form.password.data)
        flash(_("Your password has been reset."))
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password.html", form=form)
