from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from services.analysis_orchestrator import analyze_journal

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# -------------------
# Models
# -------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    journals = db.relationship("JournalEntry", backref="user", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    journal_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    analyses = db.relationship("JournalAnalysisRow", backref="journal", lazy=True, cascade="all, delete-orphan")


class JournalAnalysisRow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    life_area = db.Column(db.String(100), nullable=True)
    chunk_text = db.Column(db.Text, nullable=True)
    reaction_pattern = db.Column(db.String(200), nullable=True)
    percent = db.Column(db.Float, nullable=True)
    emotion = db.Column(db.String(100), nullable=True)

    journal_entry_id = db.Column(db.Integer, db.ForeignKey("journal_entry.id"), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# -------------------
# Routes
# -------------------
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    journal_text = ""
    analysis_rows = []

    if request.method == "POST":
        journal_text = request.form.get("journal_text", "").strip()

        if journal_text:
            analysis_rows = analyze_journal(journal_text)

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


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            flash("Username or email already exists.", "danger")
            return redirect(url_for("register"))

        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash("Login successful.", "success")
            return redirect(url_for("index"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out.", "info")
    return redirect(url_for("login"))


@app.route("/history")
@login_required
def history():
    entries = JournalEntry.query.filter_by(user_id=current_user.id) \
        .order_by(JournalEntry.created_at.desc()).all()
    return render_template("history.html", entries=entries)


@app.route("/history/<int:entry_id>")
@login_required
def history_detail(entry_id):
    entry = JournalEntry.query.get_or_404(entry_id)

    if entry.user_id != current_user.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for("history"))

    return render_template("history_detail.html", entry=entry)


@app.route("/delete-entry/<int:entry_id>", methods=["POST"])
@login_required
def delete_entry(entry_id):
    entry = JournalEntry.query.get_or_404(entry_id)

    if entry.user_id != current_user.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for("history"))

    db.session.delete(entry)
    db.session.commit()
    flash("Entry deleted.", "info")
    return redirect(url_for("history"))


if __name__ == "__main__":
    print("Starting Flask app...")

    with app.app_context():
        print("Creating database tables if they do not exist...")
        db.create_all()
        print("Database is ready.")

        print("User count:", User.query.count())
        print("Journal count:", JournalEntry.query.count())

    print("Flask app is running on http://127.0.0.1:5000")
    app.run(debug=True)