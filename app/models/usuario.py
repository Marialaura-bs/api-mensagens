from app import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    nome= db.Column(db.String(255), nullable=False)
    senha= db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "nome": self.nome,
            "senha": self.senha
        }