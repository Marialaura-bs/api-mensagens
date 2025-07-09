from flask import Blueprint, request
from ..models.message import Message
from .. import db
from ..schemas.message_schema import MessageSchema
from ..models.comentario import Comentario
from ..schemas.comentario_schema import ComentarioSchema

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
    data = MessageSchema.load(request.get_json())
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
    data = message_schema.load(request.get_json(), partial=True)#esse partial=True é necessário?

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

comentario_schema = ComentarioSchema()
comentarios_schema = ComentarioSchema(many=True)

@messages_bp.route('/<int:message_id>/comentarios', methods=['GET'])
def get_comentarios(message_id):
    comentarios = Comentario.query.filter_by(mensagem=message_id).all()
    return comentarios_schema.jsonify(comentarios), 200

@messages_bp.route('/<int:message_id>/comentarios', methods=['POST'])
def create_comentario(message_id):
    data = request.get_json()
    message=Message.query.get_or_404(message_id)
    # Cria nova mensagem vinculando ao usuário de ID 1
    novo_comentario = Comentario(
        content=data.get('content'),
        autor=1,  # <- usuário padrão
        mensagem=message_id
    )
    db.session.add(novo_comentario)
    db.session.commit()
    return comentario_schema.jsonify(novo_comentario), 201

@messages_bp.route('/<int:message_id>/comentarios/<int:comentario_id>', methods=['PUT'])
def update_comentario(message_id, comentario_id):
    message=Message.query.get_or_404(message_id)
    comentario = Comentario.query.get_or_404(comentario_id)
    data = comentario_schema.load(request.get_json(), partial=True)#por que o message_id não é atualizado?

    if 'content' in request.get_json():
        comentario.content = data.content

    db.session.commit()
    return comentario_schema.jsonify(comentario), 200

@messages_bp.route('/<int:message_id>comentarios/<int:comentario_id>', methods=['DELETE'])
def delete_comentario(message_id, comentario_id):
    message = Message.query.get_or_404(message_id)
    comentario = Comentario.query.get_or_404(comentario_id)
    db.session.delete(message)
    db.session.commit()
    return '', 204