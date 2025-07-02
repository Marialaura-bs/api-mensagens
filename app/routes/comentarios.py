from flask import Blueprint, request
from ..models.comentario import Comentario
from .. import db
from ..schemas.comentario_schema import ComentarioSchema
from app.routes.messages import messages_bp


comentario_schema = ComentarioSchema()
comentarios_schema = ComentarioSchema(many=True)

@messages_bp.route('/<int:message_id>/comentarios', methods=['GET'])
def get_comentario(message_id):
    comentario = Comentario.query.get_or_404(message_id)
    return comentario_schema.jsonify(comentario), 200

@messages_bp.route('/<int:message_id>/comentarios/<int:comentario_id>', methods=['GET'])
def get_comentario(comentario_id):
    comentario = Comentario.query.get_or_404(comentario_id)
    return comentario_schema.jsonify(comentario), 200

@messages_bp.route('/<int:message_id>/comentarios', methods=['POST'])
def create_comentario(message_id):
    data = request.get_json()

    # Cria nova mensagem vinculando ao usuário de ID 1
    if message_id:
        novo_comentario = Comentario(
            content=data.get('content'),
            autor=1  # <- usuário padrão,
            mensagem=message_id
        )

    db.session.add(novo_comentario)
    db.session.commit()

    return comentario_schema.jsonify(novo_comentario), 201