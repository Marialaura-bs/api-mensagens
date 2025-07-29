from ..models.usuario import Usuario
from .. import db

def listar_usuarios():
    return User.query.all()

def obter_usuario(user_id):
    return User.query.get(user_id)

def criar_usuario(dados):
    novo = User(**dados)
    db.session.add(novo)
    db.session.commit()
    return novo

def atualizar_usuario(usuario, dados):
    for chave, valor in dados.items():
        setattr(usuario, chave, valor)
    db.session.commit()
    return usuario

def deletar_usuario(usuario):
    db.session.delete(usuario)
    db.session.commit()

