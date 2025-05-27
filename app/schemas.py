from pydantic import BaseModel

class EstoqueBase(BaseModel):
    produto: str
    local: str
    quantidade: int

class StockCreate(EstoqueBase):
    name:str
    city:str
    uf:str
    zip_code: str
    address: str
    creation_date: str


class StockOut(EstoqueBase):
    id: int

    class Config:
        orm_mode = True
