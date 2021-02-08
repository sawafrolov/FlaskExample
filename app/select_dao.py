from flask import current_app
from flask_login import current_user
from app.models import followers, User, Post, Message, Dialog


class PaginationResult:

    items = []
    has_next = False
    has_prev = False

    def __init__(self, items, has_next, has_prev):
        self.items = items
        self.has_next = has_next
        self.has_prev = has_prev


def paginate_result(result, page):
    paginated_posts = result.paginate(page, current_app.config["POSTS_PER_PAGE"], False)
    return PaginationResult(paginated_posts.items, paginated_posts.has_next, paginated_posts.has_prev)


def select_all_users(page):
    users = User.query.order_by(User.last_seen.desc())
    return paginate_result(users, page)


def select_user_by_id(id):
    return User.query.get(int(id))


def select_user_by_username(username):
    return User.query.filter_by(username=username).first_or_404()


def select_user_by_email(email):
    return User.query.filter_by(email=email).first_or_404()


def select_current_user_followed_posts(page):
    posts = Post.query.join(
        followers, (followers.c.followed_id == Post.user_id)
    ).filter(
        followers.c.follower_id == current_user.id
    ).order_by(
        Post.timestamp.desc()
    )
    return paginate_result(posts, page)


def select_user_posts(user, page):
    posts = user.posts.order_by(Post.timestamp.desc())
    return paginate_result(posts, page)


def select_searched_posts(text, page):
    ids, total = Post.search(text, page)
    if total == 0:
        return PaginationResult([], False, False), 0
    posts = Post.query.filter(Post.id.in_(ids)).order_by(Post.timestamp.desc())
    has_next = total > page * current_app.config["POSTS_PER_PAGE"]
    has_prev = page > 1
    return PaginationResult(posts, has_next, has_prev), total


def select_dialogs(page):
    dialogs = current_user.dialogs.order_by(Dialog.last_message.desc())
    return paginate_result(dialogs, page)


def select_messages(username, page):
    user = select_user_by_username(username)
    s = current_user.messages_sent.filter_by(recipient_id=user.id)
    r = current_user.messages_received.filter_by(sender_id=user.id)
    messages = s.union(r).order_by(Message.timestamp.desc())
    return paginate_result(messages, page)
