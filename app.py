from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from services.predictor_service import hybrid_predict

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

    journals = db.relationship("JournalEntry", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    journal_text = db.Column(db.Text, nullable=False)
    reaction_pattern = db.Column(db.String(200), nullable=True)
    score = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


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
    top_label = None
    top_score = None

    if request.method == "POST":
        journal_text = request.form.get("journal_text", "").strip()

        if journal_text:
            results = hybrid_predict(journal_text, top_k=1, alpha=0.6)

            if results:
                top_label = results[0][0]
                top_score = round(results[0][1] * 100, 2)

                entry = JournalEntry(
                    journal_text=journal_text,
                    reaction_pattern=top_label,
                    score=top_score,
                    user_id=current_user.id
                )
                db.session.add(entry)
                db.session.commit()

                flash("Analysis saved successfully.", "success")

    return render_template(
        "index.html",
        journal_text=journal_text,
        top_label=top_label,
        top_score=top_score
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
        else:
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
    with app.app_context():
        db.create_all()
    app.run(debug=True)