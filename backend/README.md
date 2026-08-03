# CodeMind AI Backend

CodeMind AI is an AI-powered Engineering Knowledge Workspace.
This is the backend repository for the application.

## Tech Stack
- Python 3.13
- FastAPI
- SQLAlchemy 2.x (Async)
- PostgreSQL
- Alembic
- Pydantic V2

## Setup Instructions

1. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Setup**
   ```bash
   cp .env.example .env
   ```
   *Edit `.env` and set your `DATABASE_URL` appropriately.*

4. **Run Application**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Run Migrations (when available)**
   ```bash
   alembic upgrade head
   ```
