from flask import render_template, flash, redirect, url_for, request, jsonify, g
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import translator
from app.main import bp
from app.main.forms import EmptyForm, PostForm, EditProfileForm, SearchForm
from app.dao import add_post, update_last_seen, update_user_profile, is_following, follow_to_user, unfollow_to_user
from app.select_dao import select_user_by_username, select_all_posts, select_user_followed_posts
from app.select_dao import select_user_posts, select_searched_posts


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


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        update_last_seen(current_user)
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
        add_post(form.post.data, current_user, language)
        flash(_("Your post was published!"))
        return redirect(url_for("main.index"))
    page = get_page()
    posts = select_user_followed_posts(current_user, page)
    next_url, prev_url = get_next_and_prev("main.index", posts, page)
    return render_template(
        "main/index.html",
        title=_("Home"),
        form=form,
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url
    )


@bp.route("/explore")
@login_required
def explore():
    page = get_page()
    posts = select_all_posts(page)
    next_url, prev_url = get_next_and_prev("main.explore", posts, page)
    return render_template(
        "main/index.html",
        title=_("Explore"),
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url
    )


@bp.route("/search")
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for("main.explore"))
    page = get_page()
    posts, total = select_searched_posts(g.search_form.q.data, page)
    next_url, prev_url = get_next_and_prev("main.search", posts, page)
    return render_template(
        "main/search.html",
        title=_("Search"),
        total=total,
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url
    )


@bp.route("/user/<username>")
@login_required
def user(username):
    user = select_user_by_username(username)
    if user is None:
        flash(_("User %(username)s not found.", username=username))
        return redirect(url_for("main.index"))
    form_url = "main.edit_profile"
    form_text = _("Edit")
    if user != current_user:
        if is_following(current_user, user):
            form_url = "main.unfollow"
            form_text = _("Unfollow")
        else:
            form_url = "main.follow"
            form_text = _("Follow")
    page = get_page()
    posts = select_user_posts(user, page)
    next_url, prev_url = get_next_and_prev("main.user", posts, page, user.username)
    form = EmptyForm()
    return render_template(
        "main/user.html",
        user=user,
        form=form,
        form_url=form_url,
        form_text=form_text,
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url
    )


@bp.route("/edit_profile/<username>", methods=["GET", "POST"])
@login_required
def edit_profile(username):
    if username != current_user.username:
        flash(_("System error: This is not your username."))
        return redirect(url_for("main.index"))
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        update_user_profile(current_user, form.username.data, form.about_me.data)
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
        user = select_user_by_username(username)
        if user is None:
            flash(_("User %(username)s not found.", username=username))
            return redirect(url_for("main.index"))
        if user == current_user:
            flash(_("You cannot follow yourself!"))
            return redirect(url_for("main.user", username=username))
        follow_to_user(current_user, user)
        flash(_("You are following %(username)s!", username=username))
        return redirect(url_for("main.user", username=username))
    else:
        return redirect(url_for("main.index"))


@bp.route("/unfollow/<username>", methods=["POST"])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = select_user_by_username(username)
        if user is None:
            flash(_("User %(username)s not found.", username=username))
            return redirect(url_for("main.index"))
        if user == current_user:
            flash(_("You cannot unfollow yourself!"))
            return redirect(url_for("main.user", username=username))
        unfollow_to_user(current_user, user)
        flash(_("You are not following %(username)s.", username=username))
        return redirect(url_for("main.user", username=username))
    else:
        return redirect(url_for("main.index"))
