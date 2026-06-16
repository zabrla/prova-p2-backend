import os
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel, Field

database_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/ecommerce")
engine = create_engine(database_url)
sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

class produtodb(base):
    __tablename__ = "produtos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, default=0)
    ativo = Column(Boolean, default=True)

class produtocreate(BaseModel):
    nome: str = Field(..., min_length=1)
    preco: float = Field(..., gt=0)
    estoque: int = Field(default=0)
    ativo: bool = Field(default=True)

class produtoresponse(produtocreate):
    id: int
    model_config = {"from_attributes": True}

app = FastAPI()

base.metadata.create_all(bind=engine)

@app.get("/produtos", response_model=list[produtoresponse], status_code=status.HTTP_200_OK)
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(produtodb).all()

@app.post("/produtos", response_model=produtoresponse, status_code=status.HTTP_201_CREATED)
def criar_produto(produto: produtocreate, db: Session = Depends(get_db)):
    db_produto = produtodb(**produto.model_dump())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

@app.get("/produtos/{id}", response_model=produtoresponse, status_code=status.HTTP_200_OK)
def buscar_produto(id: int, db: Session = Depends(get_db)):
    produto = db.query(produtodb).filter(produtodb.id == id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="produto não encontrado")
    return produto

@app.delete("/produtos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_produto(id: int, db: Session = Depends(get_db)):
    produto = db.query(produtodb).filter(produtodb.id == id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="produto não encontrado")
    
    db.delete(produto)
    db.commit()
    return None