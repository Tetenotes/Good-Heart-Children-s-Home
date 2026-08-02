from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "warning"
csrf = CSRFProtect()


def create_app(config_object="app.config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.config["UPLOAD_FOLDER"].mkdir(parents=True, exist_ok=True)
    (app.config["UPLOAD_FOLDER"].parents[2] / "instance").mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app.auth import auth_bp
    from app.routes import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

    return app