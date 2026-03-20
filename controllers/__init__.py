from .auth_controller import auth_bp
from .journal_controller import journal_bp
from .history_controller import history_bp
from .dashboard_controller import dashboard_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(journal_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(dashboard_bp)