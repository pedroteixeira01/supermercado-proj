# Supermercado Viva

Projeto completo de desenvolvimento web para uma empresa fictícia do setor de supermercados. O sistema é composto por um frontend responsivo (HTML, CSS e JavaScript puros) e um backend em Python com **FastAPI**, com suporte a autenticação JWT, controle de acesso por papéis (RBAC), carrinho de compras e painel administrativo.

## Arquitetura do Projeto

```
company_site/
├── frontend/
│   ├── components/
│   │   ├── header.html        # Header injetado dinamicamente
│   │   └── footer.html        # Footer injetado dinamicamente
│   ├── css/
│   │   └── style.css
│   ├── images/
│   │   └── logo.svg
│   ├── js/
│   │   ├── main.js            # Compartilhado — header, carrinho, autenticação
│   │   ├── login.js           # Lógica da página de login
│   │   ├── produtos.js        # Lógica da página de produtos
│   │   ├── checkout.js        # Lógica da página de checkout
│   │   └── painel.js          # Lógica do painel administrativo
│   ├── index.html
│   ├── login.html
│   ├── produtos.html
│   ├── checkout.html
│   ├── painel.html
│   ├── novidades.html
│   ├── sobre.html
│   └── contato.html
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py        # Dependências de autenticação e autorização
│   │   │   └── v1/endpoints/
│   │   │       ├── auth.py
│   │   │       ├── products.py
│   │   │       ├── orders.py
│   │   │       └── users.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── security.py    # JWT e hashing de senhas
│   │   ├── db/
│   │   │   ├── database.py
│   │   │   └── models.py      # Modelos SQLAlchemy
│   │   ├── schemas/           # Schemas Pydantic
│   │   └── factory.py         # Criação da aplicação FastAPI
│   ├── alembic/               # Migrações do banco de dados
│   ├── tests/
│   └── pyproject.toml
├── docs/
│   ├── der.d2                 # Diagrama ER (formato D2)
│   └── der.png
└── docker-compose.yml
```

### Frontend (`/frontend`)

7 páginas servidas via Nginx. Header e footer são componentes reutilizáveis injetados via JavaScript. Cada página possui seu próprio arquivo `.js` com a lógica específica, sem scripts inline no HTML.

| Página | Script | Descrição |
|---|---|---|
| `index.html` | — | Página inicial com hero e cards de destaque |
| `produtos.html` | `produtos.js` | Catálogo com botão "Adicionar ao Carrinho" |
| `checkout.html` | `checkout.js` | Resumo e confirmação do pedido (requer login) |
| `painel.html` | `painel.js` | Painel admin — gerenciar produtos e usuários (requer role `admin`) |
| `login.html` | `login.js` | Autenticação de usuários |
| `novidades.html` | — | Feed de notícias |
| `sobre.html` / `contato.html` | — | Institucional e formulário de contato |

**Funcionalidades:**
- Carrinho persistido em `localStorage` (adicionar, remover, alterar quantidade)
- Popup lateral do carrinho com total e botão de checkout
- Link "Painel" no navbar visível apenas para usuários com role `admin`
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
| `GET` | `/api/v1/products/categories` | — | Lista categorias disponíveis |
| `POST` | `/api/v1/orders/` | JWT | Cria pedido para o usuário logado |
| `GET` | `/api/v1/users/` | JWT + role `admin` | Lista todos os usuários |
| `POST` | `/api/v1/users/` | JWT + role `admin` | Cria novo usuário comum |

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

# Aplicar migrações (cria e popula o banco de dados)
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

O banco é populado automaticamente via migrations com produtos, categorias e um usuário administrador.

| Campo | Valor |
|---|---|
| E-mail | `admin@superviva.com` |
| Senha | `admin123` |
| Role | `admin` |

O usuário admin tem acesso ao **Painel Administrativo**, onde pode adicionar produtos e criar novos usuários comuns (role `user`).

---

## Modelo de Dados (DER)

O diagrama entidade-relacionamento completo está em [`docs/der.d2`](docs/der.d2).

| Grupo | Entidades |
|---|---|
| Autenticação | `Role`, `User` |
| Catálogo | `Category`, `Supplier`, `Product`, `Promotion`, `PromotionProduct` |
| Estoque | `Store`, `Employee`, `Inventory` |
| Pedidos | `Order`, `OrderItem` |
| Conteúdo | `News`, `ContactMessage` |
