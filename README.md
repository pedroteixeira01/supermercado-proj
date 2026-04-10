# Supermercado Viva

Este é um projeto completo de desenvolvimento web para uma empresa fictícia do setor de supermercados, o **Supermercado Viva**. O sistema é composto por um frontend responsivo e moderno (construído com HTML, CSS e JavaScript puros) e um backend robusto em Python utilizando o framework **FastAPI**.

## Arquitetura do Projeto

O repositório está dividido em duas partes principais:

- **`/frontend`**: Aplicação web com 5 páginas (Início, Sobre, Produtos, Novidades e Contato). O layout é componentizado utilizando JavaScript (Vanilla) para injetar dinamicamente o Header e o Footer, garantindo um código limpo e sem repetições. A comunicação com o backend ocorre via requisições `fetch` nativas.
- **`/backend`**: API REST desenvolvida com FastAPI. Utiliza o **uv** para gerenciamento de dependências, **SQLAlchemy** para ORM e **Alembic** para migrações de banco de dados. O banco de dados padrão é o SQLite. A API já conta com rotas de Produtos e Autenticação (OAuth2/JWT).

## Tecnologias Utilizadas

- **Frontend**: HTML5 Semântico, CSS3 (Responsivo), JavaScript (Vanilla).
- **Backend**: Python 3.10+, FastAPI, Uvicorn, SQLAlchemy, Alembic, Pydantic, Pytest.
- **Infraestrutura**: Docker e Docker Compose.

---

## Como Executar Localmente

A forma mais simples de rodar todo o ecossistema (Frontend e Backend integrados) é através do **Docker Compose**.

### Pré-requisitos
- [Docker](https://docs.docker.com/get-docker/) instalado.
- [Docker Compose](https://docs.docker.com/compose/install/) instalado.

### Passos

1. Clone o repositório ou navegue até a pasta raiz do projeto:
   ```bash
   cd company_site
   ```

2. Suba os containers do Docker em segundo plano (em modo *detached*):
   ```bash
   docker compose up --build -d
   ```

3. **Acesse as aplicações**:
   - **Frontend (Site)**: Abra [http://localhost](http://localhost) no seu navegador.
   - **Backend (API)**: A API roda na porta 8000. A documentação interativa (Swagger UI) pode ser acessada em [http://localhost:8000/docs](http://localhost:8000/docs).

### Credenciais de Teste
O banco de dados é populado automaticamente na inicialização do backend com dados fictícios (sementes/seeds) de produtos e um usuário administrador.

Para testar a tela de login na aplicação web, utilize:
- **E-mail:** `admin@superviva.com`
- **Senha:** `admin123`

---

## Desenvolvimento e Testes (Sem Docker)

Caso queira executar e modificar o código localmente sem o uso de containers:

### Backend
O gerenciador de pacotes escolhido para o backend é o **uv**.

1. Navegue até a pasta do backend:
   ```bash
   cd backend
   ```
2. Crie o ambiente virtual e instale as dependências:
   ```bash
   uv venv
   uv pip install -e .
   ```
3. Execute as migrações para criar e popular o banco de dados (`superviva.db`):
   ```bash
   uv run alembic upgrade head
   ```
4. Inicie o servidor Uvicorn:
   ```bash
   uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
5. **Rodar os Testes Unitários**:
   A suíte de testes usa o `pytest` e um banco em memória. Para rodar:
   ```bash
   uv run pytest tests/
   ```

### Frontend
Como o frontend utiliza apenas arquivos estáticos, não há processo de build. Você pode servir os arquivos usando um servidor HTTP simples na pasta `frontend`.

Exemplo com Python:
```bash
cd frontend
python3 -m http.server 80
```
*(Após rodar o comando acima, acesse http://localhost)*
