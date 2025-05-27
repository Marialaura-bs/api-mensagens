from flask import Blueprint, jsonify

messages_bp = Blueprint('messages', __name__)

@messages_bp.route("/", methods=["GET"])
def get_messages():
    return jsonify({"messages": ["Olá, mundo!", "Essa é a segunda mensagem."]})