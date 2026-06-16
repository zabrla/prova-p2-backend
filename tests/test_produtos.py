import pytest
from main import produtodb
from conftest import testingsessionlocal

def test_listar_banco_vazio(client):
    response = client.get("/produtos")
    assert response.status_code == 200
    assert response.json() == []

def test_criar_produto_persistencia(client):
    payload = {"nome": "teclado mecânico", "preco": 350.0}
    response = client.post("/produtos", json=payload)
    assert response.status_code == 201
    
    db = testingsessionlocal()
    produto_salvo = db.query(produtodb).filter(produtodb.nome == "teclado mecânico").first()
    db.close()
    
    assert produto_salvo is not None
    assert produto_salvo.preco == 350.0

def test_criar_produto_listagem(client):
    client.post("/produtos", json={"nome": "mouse gamer", "preco": 150.0})
    response = client.get("/produtos")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["nome"] == "mouse gamer"

def test_buscar_produto_sucesso(client, produto_existente):
    response = client.get(f"/produtos/{produto_existente.id}")
    assert response.status_code == 200
    assert response.json()["nome"] == "produto fixture"

def test_buscar_produto_404(client):
    response = client.get("/produtos/999")
    assert response.status_code == 404

def test_deletar_produto_204(client, produto_existente):
    response = client.delete(f"/produtos/{produto_existente.id}")
    assert response.status_code == 204

def test_deletar_produto_confirmar_get(client, produto_existente):
    client.delete(f"/produtos/{produto_existente.id}")
    response = client.get(f"/produtos/{produto_existente.id}")
    assert response.status_code == 404

def test_deletar_produto_404(client):
    response = client.delete("/produtos/999")
    assert response.status_code == 404

@pytest.mark.parametrize("payload", [
    {"nome": "", "preco": 100.0},
    {"nome": "monitor", "preco": -50.0},
    {"nome": "monitor", "preco": 0.0},
    {"preco": 100.0},
    {"nome": "monitor"}
])
def test_payload_invalido_422(client, payload):
    response = client.post("/produtos", json=payload)
    assert response.status_code == 422

def test_isolamento_banco(client):
    response = client.get("/produtos")
    assert response.status_code == 200
    assert response.json() == []