from datetime import datetime
from app import db
from app.models.usuario import Usuario

class Mensagem(db.Model):
    __tablename__ = 'mensagens'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    conteudo = db.Column(db.String(255), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "titulo":self.titulo,
            "conteudo": self.conteudo,
            "usuario_id":self.usuario_id,
            "data_criacao": self.data_criacao.isoformat()
        }