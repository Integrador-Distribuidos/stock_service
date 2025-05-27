from pydantic import BaseModel

class EstoqueBase(BaseModel):
    produto: str
    local: str
    quantidade: int

class EstoqueCreate(EstoqueBase):
    pass

class EstoqueOut(EstoqueBase):
    id: int

    class Config:
        orm_mode = True
