from flask import render_template, flash, redirect, url_for, request, jsonify, g
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import translator
from app.main import bp
from app.main.forms import EditProfileForm, EmptyForm, PostForm, SearchForm
from app.dao import add_post, update_last_seen, update_user_profile, is_following, follow_to_user, unfollow_to_user
from app.select_dao import select_user_by_username, select_all_users, select_current_user_followed_posts
from app.select_dao import select_user_posts, select_searched_posts
from app.utils import get_page, get_next_and_prev


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
        language = translator.detect(form.message.data).lang
        add_post(form.message.data, current_user, language)
        flash(_("Your post was published!"))
        return redirect(url_for("main.index"))
    page = get_page()
    posts = select_current_user_followed_posts(page)
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
    users = select_all_users(page)
    next_url, prev_url = get_next_and_prev("main.explore", users, page)
    return render_template(
        "main/explore.html",
        title=_("Explore"),
        users=users.items,
        next_url=next_url,
        prev_url=prev_url
    )


@bp.route("/search")
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for("main.index"))
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
    page = get_page()
    posts = select_user_posts(user, page)
    next_url, prev_url = get_next_and_prev("main.user", posts, page, user.username)
    is_follow = is_following(user)
    return render_template(
        "main/user.html",
        title=_("Profile ") + username,
        user=user,
        is_follow=is_follow,
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url
    )


@bp.route("/user/<username>/popup")
@login_required
def user_popup(username):
    user = select_user_by_username(username)
    is_follow = is_following(user)
    return render_template(
        "main/user_popup.html",
        user=user,
        is_follow=is_follow
    )


@bp.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        update_user_profile(current_user, form.username.data, form.about_me.data)
        flash(_("Your changes have been saved."))
        return redirect(url_for("main.user", username=current_user.username))
    form.username.data = current_user.username
    form.about_me.data = current_user.about_me
    return render_template(
        "main/edit_profile.html",
        title=_("Edit Profile"),
        form=form
    )


@bp.route("/follow/<username>", methods=["GET"])
@login_required
def follow(username):
    user = select_user_by_username(username)
    if user == current_user:
        flash(_("You cannot follow yourself!"))
        return redirect(url_for("main.user", username=username))
    follow_to_user(current_user, user)
    flash(_("You are following %(username)s!", username=username))
    return redirect(url_for("main.user", username=username))


@bp.route("/unfollow/<username>", methods=["GET"])
@login_required
def unfollow(username):
    user = select_user_by_username(username)
    if user == current_user:
        flash(_("You cannot unfollow yourself!"))
        return redirect(url_for("main.user", username=username))
    unfollow_to_user(current_user, user)
    flash(_("You are not following %(username)s.", username=username))
    return redirect(url_for("main.user", username=username))
