# api e-commerce

api rest para gerenciamento de produtos construída com fastapi, modelada com sqlalchemy e validada com pytest. orquestração de bancos postgresql locais gerida com docker compose.

## subir o banco de testes

antes de rodar a aplicação, provisione os bancos de dados:
```bash
docker-compose up -d db_test