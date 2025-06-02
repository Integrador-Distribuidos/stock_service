from sqlalchemy.orm import Session
from app import models, schemas

# -----------------------
# CRUD de Estoque
# -----------------------

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


# -----------------------
# CRUD de Produto
# -----------------------

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_all_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id_product == product_id).first()

def update_product(db: Session, product_id: int, product_data: schemas.ProductCreate):
    product = get_product(db, product_id)
    if product:
        for field, value in product_data.model_dump().items():
            setattr(product, field, value)
        db.commit()
        db.refresh(product)
    return product

def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    if product:
        db.delete(product)
        db.commit()
    return product



# CRUD para Movimentação de Estoque
def create_stock_movement(db: Session, movement: schemas.StockMovementCreate):
    db_movement = models.StockMovement(**movement.model_dump())
    db.add(db_movement)
    db.commit()
    db.refresh(db_movement)
    return db_movement

def get_all_stock_movements(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.StockMovement).offset(skip).limit(limit).all()

def get_stock_movement(db: Session, movement_id: int):
    return db.query(models.StockMovement).filter(models.StockMovement.id_movement == movement_id).first()

def get_movements_by_product(db: Session, product_id: int):
    return db.query(models.StockMovement).filter(models.StockMovement.id_product == product_id).all()
