from sqlalchemy.orm import Session
from app import models, schemas

def create_stock(db: Session, stock: schemas.StockCreate):
    db_stock = models.Stock(**stock.model_dump())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

def get_stock(db: Session, stock_id: int):
    return db.query(models.Stock).filter(models.Stock.id_store == stock_id).first()

def get_all_stocks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Stock).offset(skip).limit(limit).all()

def delete_stock(db: Session, stock_id: int):
    stock = get_stock(db, stock_id)
    if stock:
        db.delete(stock)
        db.commit()
    return stock

def update_stock(db: Session, stock_id: int, stock_data: schemas.StockCreate):
    stock = get_stock(db, stock_id)
    if stock:
        for field, value in stock_data.model_dump().items():
            setattr(stock, field, value)
        db.commit()
        db.refresh(stock)
    return stock
