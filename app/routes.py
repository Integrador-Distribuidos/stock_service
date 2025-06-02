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

#Cadastrar estoque
@router.post("/stocks/", response_model=schemas.StockOut)
def create_stock(stock: schemas.StockCreate, db: Session = Depends(get_db)):
    return crud.create_stock(db, stock)

#Consultar estoque específico
@router.get("/stocks/{id}", response_model=schemas.StockOut)
def read_stock(id: int, db: Session = Depends(get_db)):
    stock = crud.get_stock(db, id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock


#Consultar todos os estoques
@router.get("/stocks/", response_model=list[schemas.StockOut])
def read_all_stocks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_stocks(db, skip, limit)


#Alterar estoque
@router.put("/stocks/{id}", response_model=schemas.StockOut)
def update_stock(id: int, stock: schemas.StockCreate, db: Session = Depends(get_db)):
    return crud.update_stock(db, id, stock)


#Deletar estoque
@router.delete("/stocks/{id}", response_model=schemas.StockOut)
def delete_stock(id: int, db: Session = Depends(get_db)):
    return crud.delete_stock(db, id)


# ------------------------
# ROTAS DE PRODUTOS
# ------------------------


#Cadastrar produto
@router.post("/products/", response_model=schemas.ProductOut)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)


#Consultar todos os produtos
@router.get("/products/", response_model=list[schemas.ProductOut])
def read_all_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_products(db, skip, limit)


#Consultar produto específico
@router.get("/products/{id}", response_model=schemas.ProductOut)
def read_product(id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


#Alterar produto
@router.put("/products/{id}", response_model=schemas.ProductOut)
def update_product(id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.update_product(db, id, product)


#Deletar produto
@router.delete("/products/{id}", response_model=schemas.ProductOut)
def delete_product(id: int, db: Session = Depends(get_db)):
    return crud.delete_product(db, id)


# ------------------------
# ROTAS DE MOVIMENTAÇÃO DE ESTOQUE
# ------------------------
#Criar movimentação
@router.post("/stocks/movements/", response_model=schemas.StockMovementOut)
def create_movement(movement: schemas.StockMovementCreate, db: Session = Depends(get_db)):
    return crud.create_stock_movement(db, movement)

#Consultar Movimentações
@router.get("/stocks/movements/", response_model=list[schemas.StockMovementOut])
def read_all_movements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_stock_movements(db, skip, limit)

#Consultar movimentação específica
@router.get("/stocks/movements/{id}", response_model=schemas.StockMovementOut)
def read_movement(id: int, db: Session = Depends(get_db)):
    movement = crud.get_stock_movement(db, id)
    if not movement:
        raise HTTPException(status_code=404, detail="Movement not found")
    return movement


#Consultar movimentação pelo id do produto
@router.get("/stocks/movements/product/{id}", response_model=list[schemas.StockMovementOut])
def read_movements_by_product(id: int, db: Session = Depends(get_db)):
    return crud.get_movements_by_product(db, id)