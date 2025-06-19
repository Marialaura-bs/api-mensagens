from flask import Blueprint, request
from ..models.message import Message
from .. import db
from ..schemas.message_schema import MessageSchema

messages_bp = Blueprint('messages', __name__)
message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)

@messages_bp.route('/', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    return messages_schema.jsonify(messages), 200

@messages_bp.route('/<int:message_id>', methods=['GET'])
def get_message(message_id):
    message = Message.query.get_or_404(message_id)
    return message_schema.jsonify(message), 200

@messages_bp.route('/', methods=['POST'])
def create_message():
    data = request.get_json()

    # Cria nova mensagem vinculando ao usuário de ID 1
    nova_mensagem = Message(
        content=data.get('content'),
        autor=1  # <- usuário padrão
    )

    db.session.add(nova_mensagem)
    db.session.commit()

    return message_schema.jsonify(nova_mensagem), 201

@messages_bp.route('/<int:message_id>', methods=['PUT'])
def update_message(message_id):
    message = Message.query.get_or_404(message_id)
    data = message_schema.load(request.get_json(), partial=True)

    if 'content' in request.get_json():
        message.content = data.content

    db.session.commit()
    return message_schema.jsonify(message), 200

@messages_bp.route('/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    return '', 204