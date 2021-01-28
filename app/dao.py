from datetime import datetime
from app import db
from app.models import followers, User, Post


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


def is_following(user1, user2):
    return user1.followed.filter(
        followers.c.followed_id == user2.id
    ).count() > 0


def follow_to_user(user1, user2):
    if not is_following(user1, user2):
        user1.followed.append(user2)
        commit_changes()


def unfollow_to_user(user1, user2):
    if is_following(user1, user2):
        user1.followed.remove(user2)
        commit_changes()


def add_post(text, author, language):
    post = Post(body=text, author=author, language=language)
    db.session.add(post)
    commit_changes()
