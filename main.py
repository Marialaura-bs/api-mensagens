from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import Mensagem
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)
app = FastAPI()

class MensagemCreate(BaseModel):
    conteudo: str

class MensagemUpdate(BaseModel):
    conteudo: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/mensagens")
def criar_mensagem(msg: MensagemCreate, db: Session = Depends(get_db)):
    nova = Mensagem(conteudo=msg.conteudo)
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova

@app.get("/mensagens")
def listar_mensagens(db: Session = Depends(get_db)):
    return db.query(Mensagem).all()

@app.get("/mensagens/{id}")
def obter_mensagem(id: int, db: Session = Depends(get_db)):
    msg = db.query(Mensagem).get(id)
    if not msg:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    return msg

@app.put("/mensagens/{id}")
def atualizar_mensagem(id: int, dados: MensagemUpdate, db: Session = Depends(get_db)):
    msg = db.query(Mensagem).get(id)
    if not msg:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    msg.conteudo = dados.conteudo
    db.commit()
    return msg

@app.delete("/mensagens/{id}")
def deletar_mensagem(id: int, db: Session = Depends(get_db)):
    msg = db.query(Mensagem).get(id)
    if not msg:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    db.delete(msg)
    db.commit()
    return {"ok": True}
