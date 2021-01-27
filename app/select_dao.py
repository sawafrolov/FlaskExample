from flask import current_app
from app.models import followers, User, Post


class PaginationResult:

    items = []
    has_next = False
    has_prev = False

    def __init__(self):
        pass

    def __init__(self, items, has_next, has_prev):
        self.items = items
        self.has_next = has_next
        self.has_prev = has_prev


def paginate_posts(posts, page):
    paginated_posts = posts.paginate(page, current_app.config["POSTS_PER_PAGE"], False)
    return PaginationResult(paginated_posts.items, paginated_posts.has_next, paginated_posts.has_prev)


def select_user_own_posts(user):
    return Post.query.filter_by(user_id=user.id)


def select_user_by_id(id):
    return User.query.get(int(id))


def select_user_by_username(username):
    return User.query.filter_by(username=username).first()


def select_user_by_email(email):
    return User.query.filter_by(email=email).first()


def select_all_posts(page):
    posts = Post.query.order_by(Post.timestamp.desc())
    return paginate_posts(posts, page)


def select_user_followed_posts(user, page):
    followed = Post.query.join(
        followers, (followers.c.followed_id == Post.user_id)).filter(
        followers.c.follower_id == user.id)
    own = select_user_own_posts(user)
    posts = followed.union(own).order_by(Post.timestamp.desc())
    return paginate_posts(posts, page)


def select_user_posts(user, page):
    posts = select_user_own_posts(user)
    return paginate_posts(posts, page)


def select_posts_by_ids(ids):
    return Post.query.filter(Post.id.in_(ids)).order_by(Post.timestamp.desc())
