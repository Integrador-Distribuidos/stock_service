
# app/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database
#from app.database import get_db

router = APIRouter(prefix="/stocks", tags=["stocks"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.StockOut)
def create(stock: schemas.StockCreate, db: Session = Depends(get_db)):
    return crud.create_stock(db, stock)

@router.get("/{stock_id}", response_model=schemas.StockOut)
def read(stock_id: int, db: Session = Depends(get_db)):
    stock = crud.get_stock(db, stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock

@router.get("/", response_model=list[schemas.StockOut])
def read_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_stocks(db, skip, limit)

@router.put("/{stock_id}", response_model=schemas.StockOut)
def update(stock_id: int, stock: schemas.StockCreate, db: Session = Depends(get_db)):
    return crud.update_stock(db, stock_id, stock)

@router.delete("/{stock_id}", response_model=schemas.StockOut)
def delete(stock_id: int, db: Session = Depends(get_db)):
    return crud.delete_stock(db, stock_id)
