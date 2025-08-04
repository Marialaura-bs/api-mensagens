from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from ..models.usuario import Usuario
from .. import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    user = Usuario.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.senha, senha):
        return jsonify({"error": "Credenciais inválidas"}), 401

    token = create_access_token(identity=user.id)
    return jsonify({"access_token": token}), 200