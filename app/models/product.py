from datetime import datetime, date
from sqlalchemy import Column, Float, Integer, String, ForeignKey, Date
from app.database import Base
class Product(Base):
    __tablename__ = "product"
    id_product = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float, index=True)
    sku = Column(String, index=True)
    category = Column(String, index=True)
    creation_date = Column(Date, nullable=False)