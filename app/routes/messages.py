from flask import Blueprint, request, abort
from .. import db
from ..schemas.message_schema import MessageSchema
from ..schemas.comentario_schema import ComentarioSchema
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

comentario_schema = ComentarioSchema()
comentarios_schema = ComentarioSchema(many=True)

@messages_bp.route('/<int:message_id>/comentarios', methods=['GET'])
def get_comentarios(message_id):
    comentarios = Comentario.query.filter_by(mensagem=message_id).all()
    return comentarios_schema.jsonify(comentarios), 200

@messages_bp.route('/<int:message_id>/comentarios/<int:comentario_id>', methods=['GET'])
def get_comentario(message_id, comentario_id):
    mensagem=Message.query.get(message_id)
    if not mensagem:
        abort(404)
    comentario=Comentario.query.get(comentario_id)
    return comentario_schema.jsonify(comentario), 200

@messages_bp.route('/<int:message_id>/comentarios', methods=['POST'])
def create_comentario(message_id):
    mensagem = Message.query.get(message_id)
    if not mensagem:
        abort(404)

    data = comentario_schema.load(request.get_json())
    novo_comentario = Comentario(
        content=data.content,
        autor=1,
        mensagem=message_id
    )
    db.session.add(novo_comentario)
    db.session.commit()
    return comentario_schema.jsonify(novo_comentario), 201

@messages_bp.route('/<int:message_id>/comentarios/<int:comentario_id>', methods=['PUT'])
def update_comentario(message_id, comentario_id):
    mensagem = Message.query.get(message_id)
    if not mensagem:
        abort(404)

    comentario = Comentario.query.get_or_404(comentario_id)

    # Verifica se o comentário pertence à mensagem correta
    if comentario.mensagem != message_id:
        abort(400, description="Comentário não pertence a essa mensagem.")

    # Permite atualizações parciais (não exige todos os campos)
    data = comentario_schema.load(request.get_json(), partial=True)

    if 'content' in request.get_json():
        comentario.content = data.content 

    db.session.commit()
    return comentario_schema.jsonify(comentario), 200

@messages_bp.route('/<int:message_id>/comentarios/<int:comentario_id>', methods=['DELETE'])
def delete_comentario(message_id, comentario_id):
    mensagem=Message.query.get(message_id)
    if not mensagem:
        abort(404)
    #Excluir mensagem deve estar permitido apenas para o usuário que a criou
    comentario = Comentario.query.get_or_404(comentario_id)
    db.session.delete(comentario)
    db.session.commit()
    return '', 204