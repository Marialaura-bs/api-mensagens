from app import db

class Usuario(db.Model):
    __tablename__="usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(128), nullable=False)
    perfil = db.Column(db.String(5), default='USER')