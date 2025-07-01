from flask import Flask
from .extensions import db, migrate, login_manager, mail
from .routes.activites import activites_bp  # Blueprint activités
from .routes.auth_routes import auth  # Blueprint auth
from .routes.main import main_bp
from .routes.admin import admin_bp  # <-- Import du blueprint admin

def create_app():
    app = Flask(__name__)

    # Charger la configuration depuis config.py
    app.config.from_object('config')  # Correct !

    # Initialisation des extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    # Redirection vers login si non connecté
    login_manager.login_view = 'auth.login'

    # Enregistrement des blueprints
    app.register_blueprint(activites_bp)
    app.register_blueprint(auth)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)  # <-- Enregistrement blueprint admin

    # Création des tables
    with app.app_context():
        db.create_all()

    return app
