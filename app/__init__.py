from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.json.sort_keys = False

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)
    
    from .routes.mensagens import mensagens_bp
    app.register_blueprint(mensagens_bp, url_prefix="/mensagens")
    
    from .routes.usuarios import usuarios_bp
    app.register_blueprint(usuarios_bp, url_prefix="/usuarios")

    from .routes.comentarios import comentarios_bp
    app.register_blueprint(comentarios_bp)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Tratadores globais de erro
    register_error_handlers(app)
    register_jwt_error_handlers(jwt)

    return app

def register_error_handlers(app):

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({
            "error": "Validation Error",
            "messages": error.messages
        }), 400

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return jsonify({
            "error": error.name,
            "message": error.description
        }), error.code

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        return jsonify({
            "error": "Internal Server Error",
            "message": str(error)
        }), 500

def register_jwt_error_handlers(jwt):
    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        return jsonify({"error": "Token JWT ausente ou inválido", "message": error}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"error": "Token JWT inválido", "message": error}), 422

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"error": "Token JWT expirado", "message": "Renove o token"}), 401

    @jwt.revoked_token_loader
    def wrong_token_callback(error):
        return jsonify({"error": "Tipo de token inválido", "message": error}), 422