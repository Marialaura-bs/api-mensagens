from flask import Blueprint, request, jsonify
from .. import db
from ..schemas.mensagem_schema import MessageSchema
from ..controllers import message_controller
from ..controllers import usuario_controller
from ..middlewares.message_required import mensagem_existe
from flask_jwt_extended import jwt_required, get_jwt_identity

mensagens_bp = Blueprint('mensagens', __name__)
message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)

@mensagens_bp.route('/', methods=['GET'])
def get_messages():
    messages = message_controller.listar_mensagens()
    return messages_schema.jsonify(messages), 200

@mensagens_bp.route('/<int:mensagem_id>', methods=['GET'])
@mensagem_existe
def get_message(mensagem_id):
    return message_schema.jsonify(request.mensagem), 200

@mensagens_bp.route('/', methods=['POST'])
@jwt_required()
def create_message():
    user_id = get_jwt_identity()
    data = message_schema.load(request.get_json())
    data['usuario_id'] = user_id
    message = message_controller.criar_mensagem(data)
    return message_schema.jsonify(message), 201


@mensagens_bp.route('/<int:mensagem_id>', methods=['PUT'])
@jwt_required()
@mensagem_existe
def update_message(mensagem_id):
    if request.mensagem.usuario_id != int(get_jwt_identity()):
        return jsonify({"error": "Você não tem permissão para alterar esta mensagem."}), 403
    data = message_schema.load(request.get_json())  # Atualização completa
    updated = message_controller.atualizar_mensagem(request.mensagem, data)
    return message_schema.jsonify(updated), 200

@mensagens_bp.route('/<int:mensagem_id>', methods=['PATCH'])
@jwt_required()
@mensagem_existe
def partial_update_message(mensagem_id):
    if request.mensagem.usuario_id != int(get_jwt_identity()):
        return jsonify({"error": "Você não tem permissão para alterar esta mensagem."}), 403
    data = message_schema.load(request.get_json(), partial=True)  # Atualização parcial
    updated = message_controller.atualizar_mensagem(request.mensagem, data)
    return message_schema.jsonify(updated), 200

@mensagens_bp.route('/<int:mensagem_id>', methods=['DELETE'])
@jwt_required()
@mensagem_existe
def delete_message(mensagem_id):
    user_id = get_jwt_identity()
    user = usuario_controller.obter_usuario(user_id)
    if request.mensagem.usuario_id != int(get_jwt_identity()) and user.perfil!='ADMIN':
        return jsonify({"error": "Você não tem permissão para excluir esta mensagem."}), 403
    message_controller.deletar_mensagem(request.mensagem)
    return '', 204