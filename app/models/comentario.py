from datetime import datetime
from app import db
from app.models.usuario import Usuario
from app.models.message import Message

class Comentario(db.Model):
    __tablename__ = 'comentarios'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    autor = db.Column(db.Integer, db.ForeignKey('users.id'))
    mensagem = db.Column(db.Integer, db.ForeignKey('messages.id'))

    def to_dict(self):
        return {
            "id": self.id,
            "autor":self.autor,
            "mensagem":self.mensagem,
            "content": self.content,
            "created_at": self.created_at.isoformat()
        }