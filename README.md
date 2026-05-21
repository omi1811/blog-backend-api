# 📝 Blog Backend API (FastAPI + PostgreSQL)

A production-pattern REST API with relational data modeling, migrations, and cascade deletes.

## 🚀 Features
✅ **PostgreSQL + Docker** → Persistent, isolated database  
✅ **SQLAlchemy ORM** → Pythonic data access, no raw SQL  
✅ **Alembic Migrations** → Version-controlled schema evolution  
✅ **Relational Design** → `User` ↔ `Posts` ↔ `Comments` with foreign keys  
✅ **Cascade Deletes** → Auto-cleanup of orphaned records  
✅ **FastAPI Dependencies** → Reusable, safe DB session injection  
✅ **Pydantic Validation** → Type-safe request/response contracts  

## 🛠️ Tech Stack
- **Backend**: FastAPI, SQLAlchemy, Alembic, Pydantic
- **Database**: PostgreSQL (Docker)
- **Migrations**: Alembic (auto-generate + apply)
- **Security**: Password hashing (Argon2), authorization checks

## 📦 Local Setup
```bash
# Start database
docker compose up -d

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start API
uvicorn src.main:app --reload