# 🚀 FastAPI com Docker e PostgreSQL

Este projeto é uma API moderna e leve construída com **FastAPI**, containerizada com **Docker**, e conectada a um banco de dados **PostgreSQL** com persistência de dados.

---

## 📦 Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Uvicorn](https://www.uvicorn.org/)

---

## ⚙️ Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/stock_service.git
cd stock_service


.
├── app
│   ├── main.py          # Ponto de entrada da aplicação FastAPI
│   ├── models.py        # Modelos do banco de dados
│   ├── routes.py        # Rotas da API
│   └── ...
├── requirements.txt     # Dependências Python
├── Dockerfile           # Imagem da aplicação FastAPI
├── docker-compose.yml   # Orquestração dos containers
└── README.md            # Este arquivo ✨



Endpoints da API

ESTOQUES
| Método | Endpoint                  | Descrição                              |
| ------ | ------------------------- | -------------------------------------- |
| POST   | `/api/stocks/`            | Criar um novo registro de estoque      |
| GET    | `/api/stocks/`            | Listar todos os estoques               |
| GET    | `/api/stocks/{id}/`       | Detalhar um estoque específico         |
| GET    | `/api/stocks/store/{id}/` | Listar estoques de uma loja específica |
| PUT    | `/api/stocks/{id}/`       | Atualizar dados de um estoque          |
| DELETE | `/api/stocks/{id}/`       | Deletar um registro de estoque         |

PRODUTOS
| Método | Endpoint             | Descrição                       |
| ------ | -------------------- | ------------------------------- |
| POST   | `/api/products/`     | Criar novo produto              |
| GET    | `/api/products/`     | Listar todos os produtos        |
| GET    | `/api/products/{id}` | Detalhar um produto específico  |
| PUT    | `/api/products/{id}` | Atualizar um produto específico |
| DELETE | `/api/products/{id}` | Deletar um produto específico   |


MOVIMENTAÇÃO DE ESTOQUE
| Método | Endpoint                              | Descrição                                     |
| ------ | ------------------------------------- | --------------------------------------------- |
| POST   | `/api/stocks/movements/`              | Criar nova movimentação manual de estoque     |
| GET    | `/api/stocks/movements/`              | Listar todas as movimentações                 |
| GET    | `/api/stocks/movements/{id}/`         | Detalhar uma movimentação                     |
| GET    | `/api/stocks/movements/product/{id}/` | Listar movimentações de um produto específico |





1° Apresentação do Integrador - Requisitos
1 - casos de uso
2 - arquitetura
3 - modelo lógico
4 - endpoints
