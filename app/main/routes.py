from flask import current_app, render_template, flash, redirect, url_for, request, jsonify, g
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from datetime import datetime
from app import db, translator
from app.main import bp
from app.main.forms import EmptyForm, PostForm, EditProfileForm, SearchForm
from app.models import User, Post


def paginate_posts(base_url, posts, username=""):
    page = request.args.get("page", 1, type=int)
    paginated_posts = posts.paginate(page, current_app.config["POSTS_PER_PAGE"], False)
    next_url = None
    if paginated_posts.has_next:
        if username == "":
            next_url = url_for(base_url, page=paginated_posts.next_num)
        else:
            next_url = url_for(base_url, username=username, page=paginated_posts.next_num)
    prev_url = None
    if paginated_posts.has_prev:
        if username == "":
            prev_url = url_for(base_url, page=paginated_posts.prev_num)
        else:
            prev_url = url_for(base_url, username=username, page=paginated_posts.prev_num)
    return paginated_posts, next_url, prev_url


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())


@bp.route("/translate", methods=["POST"])
@login_required
def translate_text():
    text = request.form["text"]
    source_language = request.form["source_language"]
    dest_language = request.form["dest_language"]
    result = translator.translate(text, src=source_language, dest=dest_language)
    return jsonify({
        "text": result.text
    })


@bp.route("/", methods=["GET", "POST"])
@bp.route("/index", methods=["GET", "POST"])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        language = translator.detect(form.post.data).lang
        post = Post(body=form.post.data, author=current_user, language=language)
        db.session.add(post)
        db.session.commit()
        flash(_("Your post was published!"))
        return redirect(url_for("main.index"))
    posts = current_user.followed_posts()
    paginated_posts, next_url, prev_url = paginate_posts("main.index", posts)
    return render_template(
        "main/index.html",
        title=_("Home"),
        form=form,
        posts=paginated_posts.items,
        next_url=next_url,
        prev_url=prev_url
    )


@bp.route("/explore")
@login_required
def explore():
    posts = Post.query.order_by(Post.timestamp.desc())
    paginated_posts, next_url, prev_url = paginate_posts("main.explore", posts)
    return render_template(
        "main/index.html",
        title=_("Explore"),
        posts=paginated_posts.items,
        next_url=next_url,
        prev_url=prev_url
    )


@bp.route("/search")
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for("main.explore"))
    page = request.args.get("page", 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page, current_app.config['POSTS_PER_PAGE'])
    return render_template("main/search.html", title=_("Search"), posts=posts)


@bp.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_("User %(username)s not found.", username=username))
        return redirect(url_for("main.index"))
    posts = user.posts
    paginated_posts, next_url, prev_url = paginate_posts("main.user", posts, username=user.username)
    form = EmptyForm()
    return render_template(
        "main/user.html",
        user=user,
        posts=paginated_posts.items,
        next_url=next_url,
        prev_url=prev_url,
        form=form
    )


@bp.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_("Your changes have been saved."))
        return redirect(url_for("main.user", username=current_user.username))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template("main/edit_profile.html", title=_("Edit Profile"), form=form)


@bp.route("/follow/<username>", methods=["POST"])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(_("User %(username)s not found.", username=username))
            return redirect(url_for("main.index"))
        if user == current_user:
            flash(_("You cannot follow yourself!"))
            return redirect(url_for("main.user", username=username))
        current_user.follow(user)
        db.session.commit()
        flash(_("You are following %(username)s!", username=username))
        return redirect(url_for("main.user", username=username))
    else:
        return redirect(url_for("main.index"))


@bp.route("/unfollow/<username>", methods=["POST"])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(_("User %(username)s not found.", username=username))
            return redirect(url_for("main.index"))
        if user == current_user:
            flash(_("You cannot unfollow yourself!"))
            return redirect(url_for("main.user", username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(_("You are not following %(username)s.", username=username))
        return redirect(url_for("main.user", username=username))
    else:
        return redirect(url_for("main.index"))
