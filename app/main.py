from fastapi import FastAPI
from app.routes import movement, product, stock
from app.database import engine, Base

app = FastAPI(title="Serviço de Estoques")

Base.metadata.create_all(bind=engine)

app.include_router(stock.router)
app.include_router(product.router)
app.include_router(movement.router)
