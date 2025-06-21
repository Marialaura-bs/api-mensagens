from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
from flask_marshmallow import Marshmallow
'''
importa, do pacote flask_marshmallow, a classe Marshmallow, responsável por serializar e validar dados. Com ela, pode-se criar esquemas de validação de
dados a partir de models do SQLAlchemy, impondo restrições a seus campos, e tratamento de erros globais. Além disso, ela pode serializar e desserializar dados; no caso,
está sendo usada para transformar objetos Python em JSON (para criar dados) e vice-versa (para recuperar dados).

Esse pacote, flask_marshmallow, chama-se assim porque é uma extensão Flask, que integra o Marshmallow (uma biblioteca de serialização e validação de dados)
com o Flask e o Flask SQLAlchemy, um ORM.
'''
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.json.sort_keys = False

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    from .routes.messages import messages_bp
    app.register_blueprint(messages_bp, url_prefix="/messages")
    
    from .routes.usuarios import usuarios_bp
    app.register_blueprint(usuarios_bp, url_prefix="/users")


    # Tratadores globais de erro (explicados na seção 5.6)
    register_error_handlers(app)

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