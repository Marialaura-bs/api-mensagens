from flask import Blueprint, request, jsonify, abort
from ..schemas.usuario_schema import UsuarioSchema
from ..controllers import user_controller

usuarios_bp = Blueprint('users', __name__)
user_schema = UsuarioSchema()
users_schema = UsuarioSchema(many=True)

@usuarios_bp.route("/users", methods=["GET"])
def get_users():
    users = user_controller.listar_usuarios()
    return users_schema.jsonify(users), 200

@usuarios_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = user_controller.obter_usuario(user_id)
    if not user:
        abort(404, description="Usuário não encontrado.")
    return user_schema.jsonify(user), 200

@usuarios_bp.route("/users", methods=["POST"])
def create_user():
    data = user_schema.load(request.get_json())
    novo = user_controller.criar_usuario(data)
    return user_schema.jsonify(novo), 201

@usuarios_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = user_controller.obter_usuario(user_id)
    if not user:
        abort(404)
    data = user_schema.load(request.get_json(), partial=True)
    atualizado = user_controller.atualizar_usuario(user, data)
    return user_schema.jsonify(atualizado), 200

@usuarios_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = user_controller.obter_usuario(user_id)
    if not user:
        abort(404)
    user_controller.deletar_usuario(user)
    return '', 204