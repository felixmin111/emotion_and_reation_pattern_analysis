from flask import Flask

from extensions import db, login_manager
from controllers import register_blueprints
from models import User, JournalEntry


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "your-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)

    register_blueprints(app)

    return app


app = create_app()

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