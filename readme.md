# api e-commerce

[cite_start]api rest de gerenciamento de produtos construída com fastapi, modelada com sqlalchemy e validada com pytest. orquestração de bancos postgresql locais gerida com docker compose[cite: 5, 8, 9, 13, 14, 18].

## subir o banco de testes

antes de rodar a aplicação, provisione os bancos de dados:
```bash
docker-compose up -d db_test