from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from extensions import db
from models import JournalEntry

history_bp = Blueprint("history", __name__)


@history_bp.route("/history")
@login_required
def history():
    entries = JournalEntry.query.filter_by(user_id=current_user.id) \
        .order_by(JournalEntry.created_at.desc()).all()
    return render_template("history.html", entries=entries)


@history_bp.route("/history/<int:entry_id>")
@login_required
def history_detail(entry_id):
    entry = JournalEntry.query.get_or_404(entry_id)

    if entry.user_id != current_user.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for("history.history"))

    return render_template("history_detail.html", entry=entry)


@history_bp.route("/delete-entry/<int:entry_id>", methods=["POST"])
@login_required
def delete_entry(entry_id):
    entry = JournalEntry.query.get_or_404(entry_id)

    if entry.user_id != current_user.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for("history.history"))

    db.session.delete(entry)
    db.session.commit()
    flash("Entry deleted.", "info")
    return redirect(url_for("history.history"))