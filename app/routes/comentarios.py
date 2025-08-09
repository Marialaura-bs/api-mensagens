from flask import Blueprint, request
from ..schemas.comentario_schema import ComentarioSchema
from ..controllers import comment_controller
from ..middlewares.message_required import mensagem_existe
from ..middlewares.comment_required import comentario_existe
from flask_jwt_extended import jwt_required, get_jwt_identity

comentarios_bp = Blueprint('comentarios', __name__)
comment_schema = ComentarioSchema()
comments_schema = ComentarioSchema(many=True)

@comentarios_bp.route('/mensagens/<int:mensagem>/comentarios', methods=['GET'])
@mensagem_existe
def get_comments(mensagem):
    comments = comment_controller.listar_comentarios(mensagem)
    return comments_schema.jsonify(comments), 200

@comentarios_bp.route('/mensagens/<int:mensagem>/comentarios/<int:comment_id>', methods=['GET'])
@mensagem_existe
@comentario_existe
def get_comment(mensagem, comment_id):
    return comment_schema.jsonify(request.comentario), 200

@comentarios_bp.route('/mensagens/<int:message_id>/comentarios', methods=['POST'])
@jwt_required()
@mensagem_existe
def create_comment(message_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    data['mensagem_id'] = message_id
    data['usuario_id'] = user_id
    validated_data = comment_schema.load(data)
    comment = comment_controller.criar_comentario(validated_data)
    return comment_schema.jsonify(comment), 201

@comentarios_bp.route('/mensagens/<int:mensagem>/comentarios/<int:comment_id>', methods=['PUT'])
@jwt_required()
@mensagem_existe
@comentario_existe
def update_comment(mensagem, comment_id):
    if request.mensagem.usuario_id != get_jwt_identity():
        return jsonify({"error": "Acesso negado."}), 403
    data = request.get_json()
    data['mensagem'] = mensagem
    validated_data = comment_schema.load(data)
    updated = comment_controller.atualizar_comentario(request.comentario, validated_data)
    return comment_schema.jsonify(updated), 200

@comentarios_bp.route('/mensagens/<int:mensagem>/comentarios/<int:comment_id>', methods=['PATCH'])
@jwt_required()
@mensagem_existe
@comentario_existe
def partial_update_comment(mensagem, comment_id):
    if request.mensagem.user_id != get_jwt_identity():
        return jsonify({"error": "Acesso negado."}), 403
    data = request.get_json()
    validated_data = comment_schema.load(data, partial=True)
    updated = comment_controller.atualizar_comentario(request.comentario, validated_data)
    return comment_schema.jsonify(updated), 200

@comentarios_bp.route('/mensagens/<int:mensagem>/comentarios/<int:comment_id>', methods=['DELETE'])
@mensagem_existe
@comentario_existe
@jwt_required()
def delete_comment(mensagem, comment_id):
    if request.mensagem.user_id != get_jwt_identity():
        return jsonify({"error": "Acesso negado."}), 403
    comment_controller.deletar_comentario(request.comentario)
    return '', 204