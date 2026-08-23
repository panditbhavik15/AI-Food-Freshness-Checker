# Architecture Document

## AI Food Freshness Checker

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Approved |
| **Last Updated** | 2026-08-23 |

---

## 1. System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     SYSTEM ARCHITECTURE                      │
│                                                              │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────────┐   │
│  │  React    │───▶│  FastAPI      │───▶│  ML Pipeline     │   │
│  │  Frontend │◀───│  Backend      │◀───│  (MobileNetV3)   │   │
│  │  (Vite)   │    │              │    │                  │   │
│  └──────────┘    └──────┬───────┘    └──────────────────┘   │
│                         │                                    │
│                   ┌─────▼─────┐    ┌──────────────────┐     │
│                   │ PostgreSQL │    │  Object Storage   │     │
│                   │ (SQLite    │    │  (Images)         │     │
│                   │  for dev)  │    │                   │     │
│                   └───────────┘    └──────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Frontend Architecture

### Technology Stack
- **Framework**: React 18 with Vite
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Styling**: Vanilla CSS with CSS Custom Properties (design tokens)
- **State Management**: React Context + useReducer for auth; local state for components
- **Camera**: Browser MediaDevices API (getUserMedia)

### Page Structure
| Page | Route | Auth Required |
|------|-------|--------------|
| Landing/Home | `/` | No |
| Upload/Capture | `/analyze` | No |
| Analyzing (loading) | `/analyzing` | No |
| Result | `/result/:id` | No |
| History | `/history` | Yes |
| Dashboard | `/dashboard` | Yes |
| Profile/Settings | `/profile` | Yes |
| Login | `/login` | No |
| Register | `/register` | No |

### Component Hierarchy
```
App
├── Header (navigation, auth status)
├── Routes
│   ├── HomePage
│   │   ├── HeroSection
│   │   ├── HowItWorks
│   │   ├── SupportedFoods
│   │   └── CTASection
│   ├── AnalyzePage
│   │   ├── ImageUploader (drag-drop + file select)
│   │   ├── CameraCapture (getUserMedia)
│   │   └── ImagePreview
│   ├── AnalyzingPage
│   │   └── AnalysisLoader (animated)
│   ├── ResultPage
│   │   ├── FoodIdentification
│   │   ├── FreshnessGauge
│   │   ├── ConfidenceMeter
│   │   ├── ObservationsList
│   │   ├── Recommendation
│   │   ├── SafetyDisclaimer
│   │   └── CheckAnotherCTA
│   ├── HistoryPage
│   │   └── HistoryCard (repeated)
│   ├── DashboardPage
│   │   ├── StatCards
│   │   ├── FreshnessChart
│   │   ├── TopFoodsChart
│   │   └── RecentActivity
│   └── ProfilePage
│       ├── UserInfo
│       └── Preferences
└── Footer
```

---

## 3. Backend Architecture

### Technology Stack
- **Framework**: FastAPI (Python 3.11+)
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Auth**: JWT (python-jose) + bcrypt
- **Image Processing**: Pillow, OpenCV
- **Validation**: Pydantic v2
- **Server**: Uvicorn (ASGI)

### Module Structure
```
backend/app/
├── main.py              # FastAPI app, middleware, router mounting
├── core/
│   ├── config.py        # Settings from environment
│   ├── security.py      # JWT, password hashing
│   └── database.py      # SQLAlchemy engine, sessions
├── models/
│   ├── user.py          # User ORM model
│   └── analysis.py      # Analysis ORM model
├── schemas/
│   ├── user.py          # Auth request/response schemas
│   ├── analysis.py      # Analysis request/response schemas
│   └── common.py        # Shared response envelope
├── api/v1/
│   ├── router.py        # Aggregated v1 router
│   ├── analyze.py       # POST /api/v1/analyze
│   ├── auth.py          # Register, login, logout
│   ├── history.py       # GET history, GET history/{id}, DELETE
│   ├── dashboard.py     # GET dashboard stats
│   └── health.py        # GET /health
├── services/
│   ├── image_validator.py    # Format, size, dimension, quality checks
│   ├── freshness_analyzer.py # Orchestrates ML pipeline + post-processing
│   └── recommendation.py     # Maps freshness class → recommendation text
├── ml/
│   ├── preprocessor.py  # Image resize, normalize, augment
│   ├── model_loader.py  # Load TF model or mock model
│   └── inference.py     # Run prediction, extract confidence
└── utils/
    └── image_utils.py   # EXIF stripping, thumbnail generation
```

### Request Flow
```
Client Request
    │
    ▼
FastAPI Router ──▶ Input Validation (Pydantic)
    │
    ▼
Auth Middleware (JWT verification for protected routes)
    │
    ▼
Service Layer (business logic)
    │
    ▼
ML Pipeline (if analysis request)
    │
    ▼
Database (persist result)
    │
    ▼
Response Schema ──▶ JSON Response
```

---

## 4. ML Architecture

### Model Pipeline
```
Input Image (JPEG/PNG)
    │
    ▼
Preprocessing
├── Resize to 224×224
├── Normalize to [0, 1]
├── Apply augmentation (training only)
    │
    ▼
MobileNetV3 (pre-trained on ImageNet)
├── Feature extraction layers (frozen initially)
├── Custom classification head
│   ├── GlobalAveragePooling2D
│   ├── Dense(256, relu, dropout=0.3)
│   ├── Dense(128, relu, dropout=0.2)
│   └── Dense(num_classes, softmax)
    │
    ▼
Post-processing
├── Extract top prediction class
├── Extract confidence (softmax probability)
├── Apply confidence thresholds
├── Map to freshness label
├── Generate visual indicators
    │
    ▼
Result Object
```

### Classification Strategy
- **Two-stage approach**:
  1. **Food identification**: Classify which food category (8 classes) or "not food"
  2. **Freshness classification**: For identified food, classify freshness (3 classes)
- Combined: 8 foods × 3 freshness states = 24 classes + 1 "not food" = 25 total classes

### Development Mode (Mock Model)
When no trained model is available, the system uses a **clearly labeled heuristic mode**:
- Analyzes image color distribution (HSV histogram)
- Detects brown/dark ratios as spoilage indicators
- Labels all responses with `model_version: "dev-heuristic-v0.1"`
- Displays prominent UI banner: "Development Mode"

---

## 5. Database Architecture

### Entity Relationship
```
┌──────────┐       ┌──────────────┐
│   User   │───1:N─│   Analysis   │
└──────────┘       └──────────────┘
```

### Schema (PostgreSQL / SQLite)

**users**
| Column | Type | Constraints |
|--------|------|------------|
| id | UUID | PK |
| email | VARCHAR(255) | UNIQUE, NOT NULL |
| hashed_password | VARCHAR(255) | NOT NULL |
| display_name | VARCHAR(100) | |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW |
| updated_at | TIMESTAMP | NOT NULL |

**analyses**
| Column | Type | Constraints |
|--------|------|------------|
| id | UUID | PK |
| user_id | UUID | FK → users.id, NULLABLE (guest) |
| image_path | VARCHAR(500) | NOT NULL |
| thumbnail_path | VARCHAR(500) | |
| food_category | VARCHAR(50) | NOT NULL |
| freshness_class | VARCHAR(50) | NOT NULL |
| confidence | FLOAT | NOT NULL |
| observations | JSON | NOT NULL |
| recommendation | TEXT | NOT NULL |
| model_version | VARCHAR(50) | NOT NULL |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW |

---

## 6. API Architecture

### Base URL: `/api/v1`

### Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/analyze` | Optional | Analyze food image |
| POST | `/auth/register` | No | Register new user |
| POST | `/auth/login` | No | Login, get JWT |
| POST | `/auth/logout` | Yes | Logout (client-side) |
| GET | `/history` | Yes | List user's analyses |
| GET | `/history/{id}` | Yes | Get single analysis |
| DELETE | `/history/{id}` | Yes | Delete analysis |
| GET | `/dashboard` | Yes | Dashboard statistics |
| GET | `/health` | No | Health check |

### Response Envelope
```json
{
  "success": true,
  "data": { ... },
  "error": null,
  "timestamp": "2026-08-23T12:00:00Z"
}
```

---

## 7. Authentication Architecture

```
Register ──▶ Hash password (bcrypt) ──▶ Store in DB
Login ──▶ Verify password ──▶ Issue JWT (access + refresh)
Request ──▶ Extract JWT from Authorization header ──▶ Validate ──▶ Proceed
```

- Access token: 24-hour expiry
- Refresh token: 7-day expiry
- Tokens are stateless (no server-side session store for MVP)

---

## 8. Security Architecture

| Control | Implementation |
|---------|---------------|
| HTTPS | Enforced in production (reverse proxy) |
| CORS | Whitelist frontend origin |
| Rate limiting | SlowAPI on `/analyze` and `/auth/*` |
| Input validation | Pydantic schemas on all endpoints |
| File validation | Type, size, magic bytes, dimensions |
| Password storage | bcrypt with cost factor 12 |
| Secrets | Environment variables only |
| Headers | Security headers middleware |
| SQL injection | SQLAlchemy parameterized queries |
| EXIF stripping | Pillow before storage |

---

## 9. Deployment Architecture

### Development
```
Frontend: npm run dev (Vite dev server, port 5173)
Backend: uvicorn app.main:app --reload (port 8000)
Database: SQLite (local file)
```

### Production
```
┌─────────────┐    ┌─────────────┐    ┌──────────┐
│ Nginx       │───▶│ Uvicorn     │───▶│ PostgreSQL│
│ (static +   │    │ (FastAPI)   │    │          │
│  reverse    │    │             │    └──────────┘
│  proxy)     │    └─────────────┘
└─────────────┘
     │
     ▼
┌─────────────┐
│ React       │
│ (built      │
│  static)    │
└─────────────┘
```

### Docker
- `backend/Dockerfile` — Python + FastAPI
- `frontend/Dockerfile` — Node build + Nginx serve
- `docker-compose.yml` — Orchestration

---

## 10. Testing Architecture

| Layer | Tool | Scope |
|-------|------|-------|
| Backend unit | pytest | Services, utils, ML pipeline |
| Backend API | pytest + httpx | All endpoints |
| Frontend unit | Vitest | Components, hooks |
| Frontend E2E | Playwright (future) | Full user flows |
| ML | pytest | Inference, preprocessing, OOD |

---

## 11. Monitoring & Logging

### MVP
- Structured logging (Python `logging` with JSON format)
- `/health` endpoint for uptime monitoring
- Request/response timing middleware
- ML prediction logging (food, class, confidence, model version)

### Future
- Prometheus metrics
- Grafana dashboards
- Prediction drift monitoring
