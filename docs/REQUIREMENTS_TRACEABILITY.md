# Requirements Traceability Matrix

## AI Food Freshness Checker

---

## Mapping: BRD → Architecture → Phase → Module → Test → Acceptance

| BRD ID | Requirement | Architecture Component | Phase | Module/File | Test Case | Acceptance |
|--------|------------|----------------------|-------|-------------|-----------|------------|
| FR-001–006 | Image Upload | Frontend Upload Component + Backend API | 8, 9 | `frontend/src/pages/AnalyzePage.jsx`, `backend/app/api/v1/analyze.py` | API-TEST-001, FE-TEST-001 | AC-001 |
| FR-007–011 | Camera Capture | Frontend Camera Component | 9 | `frontend/src/components/CameraCapture.jsx` | FE-TEST-002 | AC-002 |
| FR-012–016 | Image Validation | Backend Image Validator Service | 8 | `backend/app/services/image_validator.py` | API-TEST-002 | AC-003 |
| FR-017–021 | Food Identification | ML Pipeline + Backend Service | 7, 8 | `backend/app/ml/inference.py`, `backend/app/services/freshness_analyzer.py` | ML-TEST-001 | AC-004 |
| FR-022–025 | Freshness Classification | ML Model + Backend Service | 7, 8 | `backend/app/ml/inference.py` | ML-TEST-002 | AC-005 |
| FR-026–029 | Confidence Score | ML Pipeline Post-processing | 7 | `backend/app/ml/inference.py` | ML-TEST-003 | AC-006 |
| FR-030–033 | Visual Explanation | Backend Service | 8 | `backend/app/services/freshness_analyzer.py` | API-TEST-003 | AC-007 |
| FR-034–038 | Recommendation | Recommendation Engine | 8 | `backend/app/services/recommendation.py` | API-TEST-004 | AC-008 |
| FR-039–042 | Food-Safety Disclaimer | Frontend + Backend | 8, 9 | `backend/app/services/recommendation.py`, `frontend/src/components/SafetyDisclaimer.jsx` | FE-TEST-003 | AC-009 |
| FR-043–049 | Authentication | Backend Auth Module | 6 | `backend/app/core/security.py`, `backend/app/api/v1/auth.py` | API-TEST-005 | AC-010 |
| FR-050–055 | Analysis History | Backend History API + Frontend | 8, 9 | `backend/app/api/v1/history.py`, `frontend/src/pages/HistoryPage.jsx` | API-TEST-006, FE-TEST-004 | AC-011 |
| FR-056–059 | Dashboard | Backend Dashboard API + Frontend | 8, 9 | `backend/app/api/v1/dashboard.py`, `frontend/src/pages/DashboardPage.jsx` | API-TEST-007, FE-TEST-005 | AC-012 |

---

## Non-Functional Requirements Mapping

| NFR ID | Requirement | Component | Verification Method |
|--------|------------|-----------|-------------------|
| NFR-001–004 | Performance | Backend, ML, Frontend | Load testing, timing instrumentation |
| NFR-005–007 | Scalability | Architecture | Architecture review, Docker compose scaling |
| NFR-008–010 | Reliability | Backend, Database | Health checks, error handling tests |
| NFR-011–014 | Maintainability | All | Code review, test coverage report |
| NFR-015–021 | Security | Backend, Frontend | Security checklist, penetration testing |
| NFR-022–025 | Accessibility | Frontend | WCAG audit, keyboard navigation test |
| NFR-026–029 | Usability | Frontend | User flow testing, responsive testing |
| NFR-030–031 | Availability | Infrastructure | Health endpoint monitoring |

---

*This matrix will be updated as development progresses and specific file paths are finalized.*
