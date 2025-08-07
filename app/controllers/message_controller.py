from ..models.mensagem import Mensagem
from .. import db

def listar_mensagens():
    return Mensagem.query.all()

def obter_mensagem(message_id):
    return Mensagem.query.get(message_id)  # Retorna None se não encontrar

def criar_mensagem(dados):
    nova = Mensagem(**dados)
    db.session.add(nova)
    db.session.commit()
    return nova

def atualizar_mensagem(message, dados):
    for chave, valor in dados.items():
        setattr(message, chave, valor)
    db.session.commit()
    return message

def deletar_mensagem(message):
    db.session.delete(message)
    db.session.commit()