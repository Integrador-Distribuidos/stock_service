from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException
from datetime import date
# -----------------------
# CRUD de Estoque
# -----------------------

def create_stock(db: Session, stock: schemas.StockCreate):
    db_stock = models.Stock(**stock.model_dump())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

def create_ProductStock(db: Session, stock: schemas.StockCreate):
    db_productstock = models.ProductStock(**stock.model_dump())
    db.add(db_productstock)
    db.commit()
    db.refresh(db_productstock)
    return db_productstock

def get_stock(db: Session, stock_id: int):
    stock = db.query(models.Stock).filter(models.Stock.id_stock == stock_id).first()
    if not stock:
        return None

    products = (
        db.query(models.Product.id_product, models.Product.name, models.ProductStock.quantity)
        .join(models.ProductStock, models.ProductStock.id_product == models.Product.id_product)
        .filter(models.ProductStock.id_stock == stock.id_stock)
        .all()
    )
    products_list = [schemas.ProductStockOutInfo(id_product=p.id_product, name=p.name, quantity=p.quantity) for p in products]

    return schemas.StockOut(
        id_stock=stock.id_stock,
        name=stock.name,
        city=stock.city,
        uf=stock.uf,
        zip_code=stock.zip_code,
        address=stock.address,
        creation_date=stock.creation_date,
        products=products_list,
    )


def get_all_stocks(db: Session, skip: int = 0, limit: int = 100):
    stocks = db.query(models.Stock).offset(skip).limit(limit).all()
    results = []

    for stock in stocks:
        products = (
            db.query(models.Product.id_product, models.Product.name, models.ProductStock.quantity)
            .join(models.ProductStock, models.ProductStock.id_product == models.Product.id_product)
            .filter(models.ProductStock.id_stock == stock.id_stock)
            .all()
        )
        products_list = [schemas.ProductStockOutInfo(id_product=p.id_product, name=p.name, quantity=p.quantity) for p in products]

        results.append(
            schemas.StockOut(
                id_stock=stock.id_stock,
                name=stock.name,
                city=stock.city,
                uf=stock.uf,
                zip_code=stock.zip_code,
                address=stock.address,
                creation_date=stock.creation_date,
                products=products_list,
            )
        )

    return results



def delete_stock(db: Session, stock_id: int):
    stock = db.query(models.Stock).filter(models.Stock.id_stock == stock_id).first()
    if stock:
        db.delete(stock)
        db.commit()
    return stock

def update_stock(db: Session, stock_id: int, stock_data: schemas.StockCreate):
    stock = db.query(models.Stock).filter(models.Stock.id_stock == stock_id).first()
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

def get_all_products_with_stock(db: Session, skip: int = 0, limit: int = 100):
    products = (
        db.query(models.Product)
        .offset(skip)
        .limit(limit)
        .all()
    )

    product_ids = [p.id_product for p in products]

    stocks = (
        db.query(models.ProductStock)
        .filter(models.ProductStock.id_product.in_(product_ids))
        .all()
    )

    stock_map = {}
    for stock in stocks:
        if stock.id_stock is not None:  # filtra estoques inválidos
            stock_map.setdefault(stock.id_product, []).append({
                "id_stock": stock.id_stock,
                "quantity": stock.quantity
            })

    return [
        {
            "id_product": p.id_product,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "sku": p.sku,
            "category": p.category,
            "creation_date": p.creation_date,
            "stocks": stock_map.get(p.id_product, [])
        }
        for p in products
    ]



def get_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id_product == product_id).first()
    if not product:
        return None

    stock_entries = (
        db.query(models.ProductStock.id_stock, models.ProductStock.quantity)
        .filter(models.ProductStock.id_product == product_id)
        .all()
    )

    return {
        "id_product": product.id_product,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "sku": product.sku,
        "category": product.category,
        "creation_date": product.creation_date,
        "stocks": [
            {"id_stock": s.id_stock, "quantity": s.quantity}
            for s in stock_entries
        ]
    }


def update_product(db: Session, product_id: int, product_data: schemas.ProductUpdate):
    product = db.query(models.Product).filter(models.Product.id_product == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encotrado!")

    # Atualiza só os campos que vieram no JSON (diferentes de None)
    update_data = product_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if hasattr(product, field):
            setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product



def delete_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id_product == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        # Apagar registros relacionados em product_stock
    db.query(models.ProductStock).filter(models.ProductStock.id_product == product_id).delete()
    db.query(models.StockMovement).filter(models.StockMovement.id_product == product_id).delete()
    try:
        db.delete(product)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Could not delete product: {str(e)}")
    return {"detail": "Product deleted"}






def create_stock_movement(db: Session, movement: schemas.StockMovementCreate):
    db_movement = models.StockMovement(**movement.model_dump())

    # Verifica se o produto existe no estoque de origem (quando aplicável)
    origin_stock = None
    if db_movement.id_stock_origin:
        origin_stock = (
            db.query(models.ProductStock)
            .filter_by(id_product=db_movement.id_product, id_stock=db_movement.id_stock_origin)
            .first()
        )
        if not origin_stock:
            raise HTTPException(status_code=400, detail="Produto não encontrado no estoque de origem.")

    # Verifica se o produto existe no estoque de destino (quando aplicável)
    destination_stock = None
    if db_movement.id_stock_destination:
        destination_stock = (
            db.query(models.ProductStock)
            .filter_by(id_product=db_movement.id_product, id_stock=db_movement.id_stock_destination)
            .first()
        )

    # Validações e movimentações por tipo
    if db_movement.movement_type == "transfer":
        # Verifica estoque origem
        if not origin_stock or origin_stock.quantity < db_movement.quantity:
            raise HTTPException(status_code=400, detail="Estoque de origem insuficiente para transferência.")

        # Debita do estoque origem
        origin_stock.quantity -= db_movement.quantity
        origin_stock.last_update_date = date.today()

        # Credita no estoque destino (cria registro se não existir)
        if destination_stock:
            destination_stock.quantity += db_movement.quantity
            destination_stock.last_update_date = date.today()
        else:
            if not db_movement.id_stock_destination:
                raise HTTPException(status_code=400, detail="Estoque de destino inválido para transferência.")
            destination_stock = models.ProductStock(
                id_product=db_movement.id_product,
                id_stock=db_movement.id_stock_destination,
                quantity=db_movement.quantity,
                last_update_date=date.today()
            )
            db.add(destination_stock)

    elif db_movement.movement_type == "in":
        # Entrada no estoque destino
        if not db_movement.id_stock_destination:
            raise HTTPException(status_code=400, detail="Estoque de destino obrigatório para entrada.")

        if destination_stock:
            destination_stock.quantity += db_movement.quantity
            destination_stock.last_update_date = date.today()
        else:
            destination_stock = models.ProductStock(
                id_product=db_movement.id_product,
                id_stock=db_movement.id_stock_destination,
                quantity=db_movement.quantity,
                last_update_date=date.today()
            )
            db.add(destination_stock)

    elif db_movement.movement_type == "out":
        # Saída do estoque origem
        if not origin_stock:
            raise HTTPException(status_code=400, detail="Produto não encontrado no estoque de origem para saída.")

        if origin_stock.quantity < db_movement.quantity:
            raise HTTPException(status_code=400, detail="Estoque insuficiente para saída.")

        origin_stock.quantity -= db_movement.quantity
        origin_stock.last_update_date = date.today()

    else:
        raise HTTPException(status_code=400, detail="Tipo de movimentação inválido.")

    # Registra a movimentação
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

def delete_movement():
    pass
