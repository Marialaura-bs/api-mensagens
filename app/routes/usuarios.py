from flask import Blueprint, request
from ..models.usuario import Usuario
from .. import db
from ..schemas.usuario_schema import UsuarioSchema

usuarios_bp = Blueprint('users', __name__)
users_schema = UsuarioSchema()
users_schema = UsuarioSchema(many=True)

@usuarios_bp.route('/', methods=['GET'])
def get_users():
    users = Usuario.query.all()
    return users_schema.jsonify(users), 200

@usuarios_bp.route('/<int:usuario_id>', methods=['GET'])
def get_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    return users_schema.jsonify(usuario), 200

@usuarios_bp.route('/', methods=['POST'])
def create_usuario():
    data = users_schema.load(request.get_json())
    db.session.add(data)
    db.session.commit()
    return users_schema.jsonify(data), 201

@usuarios_bp.route('/<int:usuario_id>', methods=['PUT'])
def update_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    data = users_schema.load(request.get_json(), partial=True)

    if 'content' in request.get_json():
        usuario.content = data.content

    db.session.commit()
    return users_schema.jsonify(usuario), 200

@usuarios_bp.route('/<int:usuario_id>', methods=['DELETE'])
def delete_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    db.session.delete(usuario)
    db.session.commit()
    return '', 204