from fastapi import FastAPI
from app.routes import router
from app.database import engine, Base

app = FastAPI(title="Serviço de Estoques")

Base.metadata.create_all(bind=engine)

app.include_router(router)
