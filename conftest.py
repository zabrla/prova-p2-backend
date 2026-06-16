import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, base, get_db, produtodb

test_database_url = os.getenv("test_database_url", "postgresql://postgres:postgres@localhost:5433/ecommerce_test")

engine_test = create_engine(test_database_url)
testingsessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

@pytest.fixture(scope="function")
def client():
    base.metadata.create_all(bind=engine_test)
    
    def override_get_db():
        db = testingsessionlocal()
        try:
            yield db
        finally:
            db.close()
            
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as c:
        yield c
        
    base.metadata.drop_all(bind=engine_test)

@pytest.fixture
def produto_existente(client):
    db = testingsessionlocal()
    novo_produto = produtodb(nome="produto fixture", preco=99.90, estoque=10, ativo=True)
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    db.close()
    return novo_produto