from app.models import followers, User, Post


class DAO:

    db = None

    def init_app(self, app):
        self.db = app.db

    def commit_changes(self):
        self.db.session.commit()

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
