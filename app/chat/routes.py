from flask import render_template, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from flask_babel import _
from app import translator
from app.chat import bp
from app.chat.forms import MessageForm
from app.dao import send_message, read_messages
from app.select_dao import select_dialogs, select_messages
from app.utils import get_page, get_next_and_prev


@bp.route("/notifications")
@login_required
def notifications():
    return jsonify({
        "count": current_user.not_read
    })


@bp.route("/write_message/<username>")
@login_required
def write_message(username):
    form = MessageForm()
    return render_template(
        "chat/write_message.html",
        title=_("Write message to ") + username,
        username=username,
        form=form
    )


@bp.route("/dialogs")
@login_required
def dialogs():
    page = get_page()
    dialogs = select_dialogs(page)
    next_url, prev_url = get_next_and_prev("chat.dialogs", dialogs, page)
    return render_template(
        "chat/dialogs.html",
        title=_("Messages"),
        dialogs=dialogs.items,
        next_url=next_url,
        prev_url=prev_url
    )


@bp.route("/messages/<username>", methods=["GET", "POST"])
@login_required
def messages(username):
    form = MessageForm()
    if form.validate_on_submit():
        language = translator.detect(form.message.data).lang
        send_message(form.message.data, username, language)
        flash(_("Your message was sent!"))
        return redirect(url_for("chat.messages", username=username))
    page = get_page()
    messages = select_messages(username, page)
    read_messages(username)
    next_url, prev_url = get_next_and_prev("chat.messages", messages, page, username)
    return render_template(
        "chat/messages.html",
        title=_("Messages from ") + username,
        form=form,
        messages=messages.items,
        next_url=next_url,
        prev_url=prev_url
    )
