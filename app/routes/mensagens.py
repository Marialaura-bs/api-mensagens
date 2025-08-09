from flask import Blueprint, request, jsonify
from .. import db
from ..schemas.mensagem_schema import MessageSchema
from ..controllers import message_controller
from ..middlewares.message_required import mensagem_existe
from flask_jwt_extended import jwt_required, get_jwt_identity

mensagens_bp = Blueprint('mensagens', __name__)
message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)

@mensagens_bp.route('/', methods=['GET'])
def get_messages():
    messages = message_controller.listar_mensagens()
    return messages_schema.jsonify(messages), 200

@mensagens_bp.route('/<int:message_id>', methods=['GET'])
@mensagem_existe
def get_message(message_id):
    return message_schema.jsonify(request.mensagem), 200

@mensagens_bp.route('/', methods=['POST'])
@jwt_required()
def create_message():
    user_id = get_jwt_identity()
    data = message_schema.load(request.get_json())
    data['usuario_id'] = user_id
    message = message_controller.criar_mensagem(data)
    return message_schema.jsonify(message), 201


@mensagens_bp.route('/<int:message_id>', methods=['PUT'])
@jwt_required()
@mensagem_existe
def update_message(message_id):
    if request.mensagem.usuario_id != get_jwt_identity():
        return jsonify({"error": "Acesso negado."}), 403
    data = message_schema.load(request.get_json())  # Atualização completa
    updated = message_controller.atualizar_mensagem(request.mensagem, data)
    return message_schema.jsonify(updated), 200

@mensagens_bp.route('/<int:message_id>', methods=['PATCH'])
@jwt_required()
@mensagem_existe
def partial_update_message(message_id):
    if request.mensagem.user_id != int(get_jwt_identity()):
        return jsonify({"error": "Acesso negado."}), 403
    data = message_schema.load(request.get_json(), partial=True)  # Atualização parcial
    updated = message_controller.atualizar_mensagem(request.mensagem, data)
    return message_schema.jsonify(updated), 200

@mensagens_bp.route('/<int:message_id>', methods=['DELETE'])
@jwt_required()
@mensagem_existe
def delete_message(message_id):
    if request.mensagem.user_id != get_jwt_identity():
        return jsonify({"error": "Acesso negado."}), 403
    message_controller.deletar_mensagem(request.mensagem)
    return '', 204