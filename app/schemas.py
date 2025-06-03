from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List

from sqlalchemy import Null
# ---------- STOCK ----------

class ProductStockInfo(BaseModel):
    id_stock: int
    quantity: int

class ProductStockOutInfo(BaseModel):
    id_product: int
    name: str
    quantity: int


class StockCreate(BaseModel):
    name: str
    city: str
    uf: str
    zip_code: str
    address: str
    creation_date: date

class StockOut(BaseModel):
    id_stock: int
    name: Optional[str] = None
    city: Optional[str] = None
    uf: Optional[str] = None
    zip_code: Optional[str] = None
    address: Optional[str] = None
    creation_date: Optional[date] = None
    products: Optional[List[ProductStockOutInfo]] = []

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
    stocks: Optional[List[ProductStockInfo]] = []
    creation_date: date

    class Config:
        orm_mode = True


class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    sku: Optional[str]
    category: Optional[str]
    creation_date: Optional[date]
    stocks: Optional[List[ProductStockInfo]]=None

    class Config:
        orm_mode = True


class ProductStock(BaseModel):
    id_product: int
    id_stock: int
    quantity: int
    last_update_date: date

class ProductStockOut(BaseModel):
    id_productstock: int
    id_product: int
    id_stock: int
    quantity: int
    last_update_date: date


class StockMovementCreate(BaseModel):
    id_product: int
    id_stock_origin: int
    id_stock_destination: int
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