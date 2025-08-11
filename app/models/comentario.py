from datetime import datetime
from app import db
from app.models.usuario import Usuario
from app.models.mensagem import Mensagem

class Comentario(db.Model):
    __tablename__ = 'comentarios'
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(255), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    mensagem_id = db.Column(db.Integer, db.ForeignKey('mensagens.id'))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    editado=db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "conteudo": self.conteudo,
            "usuario_id":self.usuario_id,
            "mensagem_id":self.mensagem_id,
            "data_criacao": self.data_criacao.isoformat()
        }