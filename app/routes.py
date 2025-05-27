from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/estoques/", response_model=schemas.EstoqueOut)
def criar(estoque: schemas.EstoqueCreate, db: Session = Depends(get_db)):
    return crud.criar_estoque(db, estoque)

@router.get("/estoques/", response_model=list[schemas.EstoqueOut])
def listar(db: Session = Depends(get_db)):
    return crud.listar_estoques(db)
