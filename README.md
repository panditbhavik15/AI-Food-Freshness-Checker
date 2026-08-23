# AI Food Freshness Checker

> **Visual AI estimate of food freshness — not a laboratory food-safety test.**

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Git

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Running Tests
```bash
# Backend pytest suite
cd backend
pytest tests/ -v
```

### Frontend
```bash
cd frontend
npm install
npm run dev
npm run build
```

### Environment
Copy `.env.example` to `.env` and configure:
```bash
cp .env.example .env
```

## Project Structure
```
food/
├── docs/           # Project documentation (BRD, Architecture, Rules, etc.)
├── backend/        # FastAPI + ML pipeline
├── frontend/       # React + Vite
├── ml/             # ML training & evaluation (future)
└── scripts/        # Utility scripts
```

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + Vite |
| Backend | Python + FastAPI |
| ML | TensorFlow/Keras (MobileNetV3) |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Auth | JWT + bcrypt |

## Documentation
- [BRD](docs/BRD.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Rules](docs/RULES.md)
- [Phase Plan](docs/PHASE_PLAN.md)
- [Dataset Strategy](docs/DATASET.md)
- [Project Context](docs/PROJECT_CONTEXT.md)

## License
Private — All rights reserved.
