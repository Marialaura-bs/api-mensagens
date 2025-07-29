from flask import Blueprint, request
from ..schemas.comentario_schema import ComentarioSchema
from ..controllers import comment_controller
from ..middlewares.message_required import mensagem_existe
from ..middlewares.comment_required import comentario_existe

comments_bp = Blueprint('comments', __name__)
comment_schema = ComentarioSchema()
comments_schema = ComentarioSchema(many=True)

@comments_bp.route('/messages/<int:mensagem>/comments', methods=['GET'])
@mensagem_existe
def get_comments(mensagem):
    comments = comment_controller.listar_comentarios(mensagem)
    return comments_schema.jsonify(comments), 200

@comments_bp.route('/messages/<int:mensagem>/comments/<int:comment_id>', methods=['GET'])
@mensagem_existe
@comentario_existe
def get_comment(mensagem, comment_id):
    return comment_schema.jsonify(request.comentario), 200

@comments_bp.route('/messages/<int:mensagem>/comments', methods=['POST'])
@mensagem_existe
def create_comment(mensagem):
    data = request.get_json()
    data['mensagem'] = mensagem
    validated_data = comment_schema.load(data)
    comment = comment_controller.criar_comentario(validated_data)
    return comment_schema.jsonify(comment), 201

@comments_bp.route('/messages/<int:mensagem>/comments/<int:comment_id>', methods=['PUT'])
@mensagem_existe
@comentario_existe
def update_comment(mensagem, comment_id):
    data = request.get_json()
    data['mensagem'] = mensagem
    validated_data = comment_schema.load(data)
    updated = comment_controller.atualizar_comentario(request.comentario, validated_data)
    return comment_schema.jsonify(updated), 200

@comments_bp.route('/messages/<int:mensagem>/comments/<int:comment_id>', methods=['PATCH'])
@mensagem_existe
@comentario_existe
def partial_update_comment(mensagem, comment_id):
    data = request.get_json()
    validated_data = comment_schema.load(data, partial=True)
    updated = comment_controller.atualizar_comentario(request.comentario, validated_data)
    return comment_schema.jsonify(updated), 200

@comments_bp.route('/messages/<int:mensagem>/comments/<int:comment_id>', methods=['DELETE'])
@mensagem_existe
@comentario_existe
def delete_comment(mensagem, comment_id):
    comment_controller.deletar_comentario(request.comentario)
    return '', 204