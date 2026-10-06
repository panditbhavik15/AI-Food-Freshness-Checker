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

MIT License

Copyright (c) 2026 Bhavik Pandit

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
