# CodeMind

![CodeMind](https://via.placeholder.com/1200x600/000000/FFFFFF?text=CodeMind)

**CodeMind** is a premium, enterprise-grade Knowledge Workspace that transforms your codebase into an intelligent, queryable vector index. Designed with the uncompromising aesthetic and performance standards of tools like Linear and Arc, CodeMind bridges the gap between raw repository data and developer understanding through advanced Retrieval-Augmented Generation (RAG).

## Features

- **Vector-Native Repository Indexing:** Connects to your repositories and indexes code into Qdrant using `text-embedding-3`.
- **Knowledge Workspace:** An IDE-like split-pane interface designed for zero-distraction focus, not gimmicky chat interfaces.
- **Exact Citation Resolution:** Responses trace directly back to exact file paths and chunk indices within your repository.
- **Monochromatic & Accessible UI:** Built on React 19, Tailwind v4, and Radix Primitives for AA-compliant accessibility and sub-100ms interactions.
- **Optimized Performance:** Aggressive code-splitting, TanStack Query server-state management, and comprehensive Error Boundary containment.

## Architecture

CodeMind is split into two independent services:

### Frontend (`/frontend`)
- **Framework:** React 19 + Vite (TypeScript)
- **State Management:** Zustand (Client state), TanStack Query (Server state)
- **Styling:** Tailwind CSS v4 + Framer Motion + Shadcn/Radix Primitives
- **Routing:** React Router v7 with route-level Suspense/Lazy loading

### Backend (`/backend`)
- **Framework:** FastAPI (Python 3.10+)
- **Database:** PostgreSQL (SQLAlchemy + Alembic)
- **Vector Store:** Qdrant
- **Authentication:** JWT (OAuth2 Password Bearer)

## Local Development

### Prerequisites
- Node.js 20+
- Python 3.10+
- Docker & Docker Compose (for Postgres and Qdrant)

### Quick Start

**1. Clone the repository**
```bash
git clone https://github.com/your-org/codemind.git
cd codemind
```

**2. Start Infrastructure (Databases)**
```bash
# Wait, Docker-compose setup pending! For now, configure Postgres locally.
```

**3. Start the Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**4. Start the Frontend**
```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

## Documentation

Full architectural documentation can be found in:
- `backend/docs/` - Backend design, API contracts, and architecture.
- `frontend/docs/` - Frontend Product Requirements (PRD), Design System, and component standards.

## Deployment Readiness

CodeMind is designed for cloud-native deployment. 
- Ensure `VITE_API_URL` is set during the frontend build step.
- Backend requires `DATABASE_URL` and `QDRANT_URL`.
- We recommend Vercel/Netlify for the Frontend, and Render/AWS for the Backend + Databases.

## License

Proprietary Software. All rights reserved.
