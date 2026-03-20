from collections import defaultdict
from flask import Blueprint, render_template
from flask_login import login_required, current_user

from extensions import db
from models import JournalEntry, JournalAnalysisRow

dashboard_bp = Blueprint("dashboard", __name__)


def normalize_label(value, fallback="Unknown"):
    if not value:
        return fallback
    return value.replace("_", " ").strip().title()

def normalize_label(value, fallback="Unknown"):
    if not value:
        return fallback
    return value.replace("_", " ").replace("-", " ").strip().title()


def normalize_emotion(emotion):
    if not emotion:
        return "Unknown"

    emotion = emotion.strip().lower()

    emotion_group_map = {
        "admiration": "Confidence",
        "approval": "Confidence",
        "gratitude": "Confidence",
        "pride": "Confidence",
        "optimism": "Confidence",
        "relief": "Confidence",

        "amusement": "Happy",
        "excitement": "Happy",
        "joy": "Happy",
        "love": "Happy",

        "caring": "Caring",
        "desire": "Caring",
        "curiosity": "Caring",

        "anger": "Disapproval",
        "annoyance": "Disapproval",
        "disapproval": "Disapproval",
        "disgust": "Disapproval",

        "disappointment": "Sadness",
        "grief": "Sadness",
        "remorse": "Sadness",
        "sadness": "Sadness",
        "embarrassment": "Sadness",

        "fear": "Anxiety",
        "nervousness": "Anxiety",
        "confusion": "Anxiety",

        "realization": "Realization",
        "surprise": "Realization",

        "neutral": "Neutral"
    }

    return emotion_group_map.get(emotion, emotion.title())

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    rows = (
        db.session.query(JournalAnalysisRow, JournalEntry.created_at)
        .join(JournalEntry, JournalAnalysisRow.journal_entry_id == JournalEntry.id)
        .filter(JournalEntry.user_id == current_user.id)
        .all()
    )

    summary_map = {}
    emotion_by_life_area = defaultdict(lambda: defaultdict(int))

    for analysis, created_at in rows:
        life_area = normalize_label(analysis.life_area)
        emotion = normalize_emotion(analysis.emotion)

        if life_area not in summary_map:
            summary_map[life_area] = {
                "count": 0,
                "emotion_total": 0,
                "emotion_score_count": 0,
                "emotion_counts": defaultdict(int)
            }

        summary_map[life_area]["count"] += 1
        summary_map[life_area]["emotion_counts"][emotion] += 1
        emotion_by_life_area[life_area][emotion] += 1

        if analysis.emotion_percent is not None:
            summary_map[life_area]["emotion_total"] += analysis.emotion_percent
            summary_map[life_area]["emotion_score_count"] += 1

    life_area_summary = []

    for life_area, data in summary_map.items():
        top_emotion = None
        top_count = 0

        for emotion, count in data["emotion_counts"].items():
            if count > top_count:
                top_emotion = emotion
                top_count = count

        avg_emotion_score = 0
        if data["emotion_score_count"] > 0:
            avg_emotion_score = round(
                data["emotion_total"] / data["emotion_score_count"], 2
            )

        life_area_summary.append({
            "life_area": life_area,
            "count": data["count"],
            "top_emotion": top_emotion,
            "avg_emotion_score": avg_emotion_score
        })

    life_area_summary.sort(key=lambda x: x["count"], reverse=True)

    return render_template(
        "dashboard.html",
        life_area_summary=life_area_summary,
        emotion_by_life_area=dict(emotion_by_life_area)
    )