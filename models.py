from sqlalchemy import Column, Integer, String
from database import Base

class Mensagem(Base):
    __tablename__ = "mensagens"
    id = Column(Integer, primary_key=True, index=True)
    conteudo = Column(String, index=True)
