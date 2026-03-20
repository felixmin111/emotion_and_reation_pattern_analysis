from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    journals = db.relationship(
        "JournalEntry",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    journal_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    analyses = db.relationship(
        "JournalAnalysisRow",
        backref="journal",
        lazy=True,
        cascade="all, delete-orphan"
    )


class JournalAnalysisRow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    life_area = db.Column(db.String(100), nullable=True)
    chunk_text = db.Column(db.Text, nullable=True)
    reaction_pattern = db.Column(db.String(200), nullable=True)
    percent = db.Column(db.Float, nullable=True)
    emotion = db.Column(db.String(100), nullable=True)
    emotion_percent = db.Column(db.Float, nullable=True)

    journal_entry_id = db.Column(
        db.Integer,
        db.ForeignKey("journal_entry.id"),
        nullable=False
    )


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))