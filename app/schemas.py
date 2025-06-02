from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional
# ---------- STOCK ----------

class StockCreate(BaseModel):
    name: str
    city: str
    uf: str
    zip_code: str
    address: str
    creation_date: date

class StockOut(BaseModel):
    id_stock: int
    name: str
    city: str
    uf: str
    zip_code: str
    address: str
    creation_date: date

    class Config:
        orm_mode = True

# ---------- PRODUCT ----------

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    sku: str
    category: str
    creation_date: date

class ProductOut(BaseModel):
    id_product: int
    name: str
    description: str
    price: float
    sku: str
    category: str
    creation_date: date

    class Config:
        orm_mode = True


class StockMovementCreate(BaseModel):
    id_movement: int
    id_product: int
    id_stock_origin: Optional[int] = None
    id_stock_destination: Optional[int] = None
    quantity: int
    observation: Optional[str] = None
    movement_type: str  
    creation_date: date

class StockMovementOut(BaseModel):
    id_movement: int
    id_product: int
    id_stock_origin: Optional[int]
    id_stock_destination: Optional[int]
    quantity: int
    observation: Optional[str]
    movement_type: str
    creation_date: date

    class Config:
        orm_mode = True