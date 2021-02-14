from flask_login import current_user
from datetime import datetime
from app import db
from app.models import followers, User, Post, Message, Dialog
from app.select_dao import select_user_by_username


def commit_changes():
    db.session.commit()


def create_user(username, password, email):
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    commit_changes()


def update_last_seen(user):
    user.last_seen = datetime.utcnow()
    commit_changes()


def update_user_profile(user, username, about):
    user.username = username
    user.about_me = about
    commit_changes()


def change_password(user, password):
    user.set_password(password)
    commit_changes()


def is_following(user):
    return current_user.followed.filter(
        followers.c.followed_id == user.id
    ).count() > 0


def follow_to_user(user):
    if not is_following(user):
        current_user.followed.append(user)
        commit_changes()


def unfollow_to_user(user):
    if is_following(user):
        current_user.followed.remove(user)
        commit_changes()


def add_post(text, author, language):
    post = Post(body=text, author=author, language=language)
    db.session.add(post)
    commit_changes()


def read_messages(username):
    user = select_user_by_username(username)
    dialog = select_dialog(user, current_user)
    dialog.recipient.not_read -= dialog.not_read
    dialog.not_read = 0
    commit_changes()


def send_message(text, username, language):
    user = select_user_by_username(username)
    dialog = select_dialog(current_user, user)
    d = select_dialog(user, current_user)
    d.last_message = datetime.utcnow()
    dialog.not_read += 1
    dialog.recipient.not_read += 1
    message = Message(body=text, author=current_user, recipient=user, language=language)
    db.session.add(message)
    commit_changes()


def select_dialog(sender, recipient):
    dialog = Dialog.query.filter_by(
        sender=sender, recipient=recipient
    ).first()
    if not dialog:
        dialog = Dialog(sender=sender, recipient=recipient)
        db.session.add(dialog)
        commit_changes()
    return dialog
