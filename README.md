# Supermercado Viva

Projeto completo de desenvolvimento web para uma empresa fictícia do setor de supermercados. O sistema é composto por um frontend responsivo (HTML, CSS e JavaScript puros) e um backend em Python com **FastAPI**, com suporte a autenticação JWT, controle de acesso por papéis (RBAC), carrinho de compras e painel administrativo.

## Arquitetura do Projeto

```
company_site/
├── frontend/          # Aplicação web estática (Nginx)
├── backend/           # API REST (FastAPI + SQLite)
├── docs/              # Documentação (DER em D2)
└── docker-compose.yml
```

### Frontend (`/frontend`)

7 páginas servidas via Nginx, componentizadas com JavaScript (header e footer injetados dinamicamente):

| Página | Descrição |
|---|---|
| `index.html` | Página inicial com hero e cards de destaque |
| `produtos.html` | Catálogo de produtos com botão "Adicionar ao Carrinho" |
| `checkout.html` | Resumo do pedido e confirmação (requer login) |
| `painel.html` | Painel administrativo — adicionar produtos (requer role `admin`) |
| `login.html` | Autenticação de usuários |
| `novidades.html` | Feed de notícias |
| `sobre.html` / `contato.html` | Institucional e formulário de contato |

**Funcionalidades do frontend:**
- Carrinho persistido em `localStorage` (add, remover, alterar quantidade)
- Popup lateral do carrinho com total e acesso ao checkout
- Link "Painel" no navbar visível apenas para admins
- Redirecionamento automático para login em páginas protegidas

### Backend (`/backend`)

API REST com FastAPI. Banco de dados SQLite gerenciado por SQLAlchemy e Alembic.

**Rotas disponíveis:**

| Método | Rota | Autenticação | Descrição |
|---|---|---|---|
| `POST` | `/api/v1/auth/login/access-token` | — | Login, retorna JWT |
| `GET` | `/api/v1/auth/me` | JWT | Dados do usuário logado (id, email, role) |
| `GET` | `/api/v1/products/` | — | Lista todos os produtos |
| `GET` | `/api/v1/products/{id}` | — | Detalhe de um produto |
| `POST` | `/api/v1/products/` | JWT + role `admin` | Cria novo produto |
| `GET` | `/api/v1/products/categories` | — | Lista categorias |
| `POST` | `/api/v1/orders/` | JWT | Cria pedido para o usuário logado |

Documentação interativa (Swagger UI): [http://localhost:8000/docs](http://localhost:8000/docs)

## Tecnologias

- **Frontend**: HTML5, CSS3 (responsivo, CSS Variables), JavaScript Vanilla
- **Backend**: Python 3.10+, FastAPI, Uvicorn, SQLAlchemy, Alembic, Pydantic, PassLib (Argon2), Python-Jose (JWT)
- **Infraestrutura**: Docker, Docker Compose, Nginx, SQLite

---

## Como Executar

### Com Docker Compose (recomendado)

**Pré-requisitos:** Docker e Docker Compose instalados.

```bash
# Na raiz do projeto
docker compose up --build -d
```

- **Frontend:** [http://localhost](http://localhost)
- **API / Swagger:** [http://localhost:8000/docs](http://localhost:8000/docs)

### Sem Docker

**Backend:**
```bash
cd backend

# Criar ambiente virtual e instalar dependências
uv venv
uv pip install -e .

# Aplicar migrações (cria e popula o banco)
uv run alembic upgrade head

# Iniciar servidor
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend:**
```bash
cd frontend
python3 -m http.server 80
# Acesse http://localhost
```

**Testes:**
```bash
cd backend
uv run pytest tests/
```

---

## Credenciais de Teste

O banco é populado automaticamente via migrations (seeds) com produtos, categorias e um usuário administrador.

| Campo | Valor |
|---|---|
| E-mail | `admin@superviva.com` |
| Senha | `admin123` |
| Role | `admin` |

> O usuário admin tem acesso ao **Painel Administrativo** e pode adicionar produtos via interface web ou diretamente pela API.

---

## Modelo de Dados (DER)

O diagrama entidade-relacionamento completo está em [`docs/der.d2`](docs/der.d2).

**Entidades principais:**

- **Role / User** — autenticação com JWT e controle de acesso por papel (`user`, `admin`)
- **Category / Supplier / Product** — catálogo de produtos
- **Promotion / PromotionProduct** — promoções com relacionamento N:N com produtos
- **Store / Employee / Inventory** — gestão de estoque por loja
- **Order / OrderItem** — pedidos realizados por usuários autenticados
- **News / ContactMessage** — conteúdo e mensagens de contato
