from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user

from extensions import db
from models import JournalEntry, JournalAnalysisRow
from utils import prettify_label
from services.analysis_orchestrator import analyze_journal

journal_bp = Blueprint("journal", __name__)


@journal_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    journal_text = ""
    analysis_rows = []

    if request.method == "POST":
        journal_text = request.form.get("journal_text", "").strip()

        if journal_text:
            analysis_rows = analyze_journal(journal_text)

            for row in analysis_rows:
                row["life_area"] = prettify_label(row.get("life_area"))
                row["reaction_pattern"] = prettify_label(row.get("reaction_pattern"))

            entry = JournalEntry(
                journal_text=journal_text,
                user_id=current_user.id
            )
            db.session.add(entry)
            db.session.flush()

            for row in analysis_rows:
                analysis = JournalAnalysisRow(
                    life_area=row.get("life_area"),
                    chunk_text=row.get("chunk_text"),
                    reaction_pattern=row.get("reaction_pattern"),
                    percent=row.get("percent"),
                    emotion=row.get("emotion"),
                    emotion_percent=row.get("emotion_percent"),
                    journal_entry_id=entry.id
                )
                db.session.add(analysis)

            db.session.commit()
            flash("Analysis saved successfully.", "success")

    return render_template(
        "index.html",
        journal_text=journal_text,
        analysis_rows=analysis_rows
    )