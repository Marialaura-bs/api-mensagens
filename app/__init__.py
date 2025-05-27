from flask import Flask

def create_app():
    app = Flask(__name__)

    # Registro de rotas
    from .routes.messages import messages_bp
    app.register_blueprint(messages_bp, url_prefix="/messages")

    return app