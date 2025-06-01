from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter(prefix="/api")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ROTAS DE ESTOQUE


@router.post("/stocks/", response_model=schemas.StockOut)
def create_stock(stock: schemas.StockCreate, db: Session = Depends(get_db)):
    return crud.create_stock(db, stock)

@router.get("/stocks/{id}", response_model=schemas.StockOut)
def read_stock(id: int, db: Session = Depends(get_db)):
    stock = crud.get_stock(db, id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock

@router.get("/stocks/", response_model=list[schemas.StockOut])
def read_all_stocks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_stocks(db, skip, limit)

@router.put("/stocks/{id}", response_model=schemas.StockOut)
def update_stock(id: int, stock: schemas.StockCreate, db: Session = Depends(get_db)):
    return crud.update_stock(db, id, stock)

@router.delete("/stocks/{id}", response_model=schemas.StockOut)
def delete_stock(id: int, db: Session = Depends(get_db)):
    return crud.delete_stock(db, id)


# ------------------------
# ROTAS DE PRODUTOS
# ------------------------

@router.post("/products/", response_model=schemas.ProductOut)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

@router.get("/products/", response_model=list[schemas.ProductOut])
def read_all_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_products(db, skip, limit)

@router.get("/products/{id}", response_model=schemas.ProductOut)
def read_product(id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/products/{id}", response_model=schemas.ProductOut)
def update_product(id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.update_product(db, id, product)

@router.delete("/products/{id}", response_model=schemas.ProductOut)
def delete_product(id: int, db: Session = Depends(get_db)):
    return crud.delete_product(db, id)


# ------------------------
# ROTAS DE MOVIMENTAÇÃO DE ESTOQUE
# ------------------------

@router.post("/stocks/movements/", response_model=schemas.StockMovementOut)
def create_movement(movement: schemas.StockMovementCreate, db: Session = Depends(get_db)):
    return crud.create_stock_movement(db, movement)

@router.get("/stocks/movements/", response_model=list[schemas.StockMovementOut])
def read_all_movements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_stock_movements(db, skip, limit)

@router.get("/stocks/movements/{movement_id}", response_model=schemas.StockMovementOut)
def read_movement(movement_id: int, db: Session = Depends(get_db)):
    movement = crud.get_stock_movement(db, movement_id)
    if not movement:
        raise HTTPException(status_code=404, detail="Movement not found")
    return movement

@router.get("/stocks/movements/product/{id}", response_model=list[schemas.StockMovementOut])
def read_movements_by_product(id: int, db: Session = Depends(get_db)):
    return crud.get_movements_by_product(db, id)



"""
| Método | Endpoint                              | Descrição                                     |
| ------ | ------------------------------------- | --------------------------------------------- |
| POST   | `/api/stocks/movements/`              | Criar nova movimentação manual de estoque     |
| GET    | `/api/stocks/movements/`              | Listar todas as movimentações                 |
| GET    | `/api/stocks/movements/{id}/`         | Detalhar uma movimentação                     |
| GET    | `/api/stocks/movements/product/{id}/` | Listar movimentações de um produto específico |"""