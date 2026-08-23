# Project Context & Memory

## AI Food Freshness Checker

---

## Current State

| Field | Value |
|-------|-------|
| **Current Phase** | Phase 4–9 (Build) |
| **Last Completed** | Phase 3 (Rules) |
| **Status** | 🔄 Building MVP |

---

## Completed Phases
- [x] Phase 0 — Discovery
- [x] Phase 1 — BRD
- [x] Phase 2 — Architecture
- [x] Phase 3 — Rules

## In Progress
- [/] Phase 4 — Project Setup
- [/] Phase 5 — Dataset Strategy
- [ ] Phase 6 — Backend Core
- [ ] Phase 7 — ML Pipeline
- [ ] Phase 8 — Backend API
- [ ] Phase 9 — Frontend

## Pending
- [ ] Phase 10 — Integration
- [ ] Phase 11 — Testing
- [ ] Phase 12 — Security
- [ ] Phase 13 — Deployment
- [ ] Phase 14 — Documentation

---

## Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Frontend framework | React 18 + Vite | Modern, fast, widely supported |
| Backend framework | FastAPI (Python) | Async, fast, built-in OpenAPI docs |
| Database (dev) | SQLite | Zero-config for development |
| Database (prod) | PostgreSQL | Relational model fits; robust |
| ORM | SQLAlchemy 2.0 | Industry standard; async support |
| Auth | JWT + bcrypt | Stateless; secure password hashing |
| ML framework | TensorFlow/Keras | Transfer learning ecosystem |
| ML model | MobileNetV3 | Lightweight; good accuracy |
| ML dev mode | Heuristic (HSV color analysis) | Clearly labeled; functional demo |
| Styling | Vanilla CSS | Full control; no framework overhead |
| Containerization | Docker | Portable; reproducible |

---

## ML Model Status

| Field | Value |
|-------|-------|
| Current model | dev-heuristic-v0.1 (development mode) |
| Architecture | Color/texture heuristic analysis |
| Production model | Pending (MobileNetV3 transfer learning) |
| Dataset | Not yet collected |
| Training status | Not started |

---

## Known Limitations
1. ML model is in development/heuristic mode — not a trained neural network
2. Only 8 food categories supported
3. Single food item per image
4. English only
5. No offline/PWA support
6. No email verification flow
7. No password reset flow

---

## Dependencies (Key)
- Python 3.11+
- Node.js 18+
- React 18
- FastAPI
- SQLAlchemy 2.0
- TensorFlow 2.x
- Pillow
- bcrypt
- python-jose (JWT)

---

## Important Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-08-23 | PostgreSQL for database | Relational model fits User/Analysis entities |
| 2026-08-23 | Guest analysis allowed | Reduce friction for first-time users |
| 2026-08-23 | 90-day image retention | Balance storage cost and user value |
| 2026-08-23 | Cloud-agnostic Docker deployment | Avoid vendor lock-in |
| 2026-08-23 | Dev heuristic mode for initial launch | Clearly labeled; follows project rules |
