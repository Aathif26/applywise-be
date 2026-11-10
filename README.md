# ApplyWise AI — Backend API

Multi-user job application management platform powered by AI.

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Language | Python 3.12+ |
| Database | PostgreSQL 16 |
| ORM | SQLAlchemy 2.x (async) |
| Migrations | Alembic |
| Auth | PyJWT + Argon2 |
| Validation | Pydantic v2 |

## Prerequisites

- Python 3.12+
- Docker & Docker Compose (for PostgreSQL)
- Git

## Local Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd applywise-be
```

### 2. Start PostgreSQL

```bash
docker compose up -d
```

This starts a Postgres 16 container on `localhost:5432` with the database
`applywise_db` (see `docker-compose.yml`).

### 3. Create & activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment

```bash
cp .env.example .env
# Edit .env — at minimum set a real JWT_SECRET_KEY
```

### 6. Run database migrations

```bash
alembic upgrade head
```

### 7. Start the development server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API is now available at **http://localhost:8000**.

- Interactive docs: http://localhost:8000/docs
- Health check: http://localhost:8000/api/v1/health
- DB health check: http://localhost:8000/api/v1/health/db

## Running Tests

```bash
pytest
```

## Project Structure

```
app/
  api/v1/           # Versioned API routers & endpoints
  core/              # Config, logging, exception handling
  db/                # SQLAlchemy engine, session, base
  models/            # ORM models (added incrementally)
  schemas/           # Pydantic request/response schemas
  repositories/      # Data access layer
  services/          # Business logic layer
  utils/             # Shared utilities
  main.py            # Application entry point

tests/               # Pytest test suite
alembic/             # Database migration scripts
docs/                # Project documentation
```

## Creating a New Migration

After adding or modifying a model:

```bash
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```

## Environment Variables

See [`.env.example`](.env.example) for the full list of configuration options.

## License

Proprietary — All rights reserved.
