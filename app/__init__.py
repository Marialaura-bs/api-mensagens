from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # aplica as configurações
    # Desativa ordenação alfabética das chaves JSON
    app.json.sort_keys = False

    db.init_app(app)  # associa o SQLAlchemy à aplicação Flask

    migrate.init_app(app, db)

    from .routes.messages import messages_bp
    app.register_blueprint(messages_bp, url_prefix="/messages")

    return app