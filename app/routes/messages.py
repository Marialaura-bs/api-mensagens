from flask import Blueprint, request
from .. import db
from ..schemas.message_schema import MessageSchema
from ..controllers import message_controller
from ..middlewares.message_required import mensagem_existe

messages_bp = Blueprint('messages', __name__)
message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)

@messages_bp.route('/', methods=['GET'])
def get_messages():
    messages = message_controller.listar_mensagens()
    return messages_schema.jsonify(messages), 200

@messages_bp.route('/<int:message_id>', methods=['GET'])
@mensagem_existe
def get_message(message_id):
    return message_schema.jsonify(request.mensagem), 200

@messages_bp.route('/', methods=['POST'])
def create_message():
    data = message_schema.load(request.get_json())
    message = message_controller.criar_mensagem(data)
    return message_schema.jsonify(message), 201

@messages_bp.route('/<int:message_id>', methods=['PUT'])
@mensagem_existe
def update_message(message_id):
    data = message_schema.load(request.get_json())  # Atualização completa
    updated = message_controller.atualizar_mensagem(request.mensagem, data)
    return message_schema.jsonify(updated), 200

@messages_bp.route('/<int:message_id>', methods=['PATCH'])
@mensagem_existe
def partial_update_message(message_id):
    data = message_schema.load(request.get_json(), partial=True)  # Atualização parcial
    updated = message_controller.atualizar_mensagem(request.mensagem, data)
    return message_schema.jsonify(updated), 200

@messages_bp.route('/<int:message_id>', methods=['DELETE'])
@mensagem_existe
def delete_message(message_id):
    message_controller.deletar_mensagem(request.mensagem)
    return '', 204