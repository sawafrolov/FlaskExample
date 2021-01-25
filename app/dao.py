from datetime import datetime
from app.models import followers, User, Post


class DAO:

    db = None

    def init_app(self, app):
        self.db = app.db

    def commit_changes(self):
        self.db.session.commit()

    def update_last_seen(self, user):
        user.last_seen = datetime.utcnow()
        self.commit_changes()

    def update_user_profile(self, user, username, about):
        user.username = username
        user.about_me = about
        self.commit_changes()

    def is_following(self, user1, user2):
        return user1.followed.filter(
            followers.c.followed_id == user2.id
        ).count() > 0

    def follow(self, user1, user2):
        if not user1.is_following(user2):
            user1.followed.append(user2)
            self.commit_changes()

    def unfollow(self, user1, user2):
        if user1.is_following(user2):
            user1.followed.remove(user2)
            self.commit_changes()

    def add_post(self, text, author, language):
        post = Post(body=text, author=author, language=language)
        self.db.session.add(post)
        self.commit_changes()
