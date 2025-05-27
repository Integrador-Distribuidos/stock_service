from sqlalchemy.orm import Session
from app import models, schemas

def criar_estoque(db: Session, estoque: schemas.EstoqueCreate):
    db_estoque = models.Estoque(**estoque.dict())
    db.add(db_estoque)
    db.commit()
    db.refresh(db_estoque)
    return db_estoque

def listar_estoques(db: Session):
    return db.query(models.Estoque).all()
