from flask import url_for, request


def get_page():
    return request.args.get("page", 1, type=int)


def get_next_and_prev(base_url, posts, page, username=""):
    next_url = None
    if posts.has_next:
        if username == "":
            next_url = url_for(base_url, page=page+1)
        else:
            next_url = url_for(base_url, username=username, page=page+1)
    prev_url = None
    if posts.has_prev:
        if username == "":
            prev_url = url_for(base_url, page=page-1)
        else:
            prev_url = url_for(base_url, username=username, page=page-1)
    return next_url, prev_url
