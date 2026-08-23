# Project Rules

## AI Food Freshness Checker

---

## 1. Coding Standards

### General
- Write clean, readable, self-documenting code
- Follow DRY (Don't Repeat Yourself) principle
- Single Responsibility Principle for all functions and classes
- Maximum function length: ~30 lines (prefer smaller)
- Maximum file length: ~300 lines (split if larger)
- Use meaningful, descriptive names for variables, functions, classes, and files

### Python (Backend)
- Follow PEP 8 style guide
- Use type hints on all function signatures
- Use Pydantic for all request/response schemas
- Use async/await for I/O-bound operations
- Docstrings on all public functions (Google style)

### JavaScript/React (Frontend)
- Use functional components with hooks
- Use `const` by default; `let` when mutation is needed; never `var`
- PropTypes or JSDoc for component props
- One component per file
- Destructure props at the function signature level

### CSS
- Use CSS custom properties (design tokens) for all colors, spacing, typography
- Mobile-first responsive design
- BEM-like naming convention for class names
- No inline styles except for dynamic values

---

## 2. Dependency Management

Before adding ANY new dependency:

1. ✅ Check if existing code/libraries already solve the problem
2. ✅ Justify WHY the dependency is needed
3. ✅ Verify the license is compatible (MIT, Apache 2.0, BSD preferred)
4. ✅ Check maintenance status (last update, open issues, downloads)
5. ✅ Record it in the appropriate requirements/package file
6. ✅ Document in CHANGELOG.md

**Never** add a dependency "just in case" or for trivial functionality.

---

## 3. Security Rules

### Secrets
- ❌ NEVER hard-code API keys, passwords, tokens, or secrets in source code
- ✅ Use environment variables for all configuration
- ✅ Provide `.env.example` with placeholder values
- ✅ Add `.env` to `.gitignore`

### Input Validation
- Validate ALL external input (API requests, file uploads, query parameters)
- Sanitize user-provided text before storage or display
- Validate file uploads: type, size, magic bytes, dimensions
- Use parameterized queries (SQLAlchemy) — never raw SQL concatenation

### Authentication
- Hash passwords with bcrypt (cost factor ≥ 12)
- Use short-lived JWT tokens
- Validate tokens on every protected request
- Return generic error messages for auth failures ("Invalid credentials")

### File Handling
- Strip EXIF metadata from uploaded images
- Store files outside the web root
- Generate unique filenames (UUID) — never use user-provided filenames
- Validate content-type matches actual file content (magic bytes)

---

## 4. Error Handling

### Rules
- ❌ NEVER silently swallow errors
- ❌ NEVER expose stack traces, internal paths, or debug info in production
- ✅ Use structured error responses with consistent format
- ✅ Log full error details server-side
- ✅ Return safe, user-friendly messages client-side

### Error Response Format
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "User-friendly description"
  }
}
```

### HTTP Status Codes
| Code | Usage |
|------|-------|
| 200 | Successful response |
| 201 | Resource created |
| 400 | Validation error, bad request |
| 401 | Authentication required |
| 403 | Forbidden (authenticated but not authorized) |
| 404 | Resource not found |
| 413 | File too large |
| 415 | Unsupported media type |
| 422 | Unprocessable entity |
| 429 | Rate limit exceeded |
| 500 | Internal server error |
| 503 | Service unavailable (e.g., model not loaded) |

---

## 5. AI/ML Rules

### Critical Rules
- ❌ NEVER fabricate model predictions
- ❌ NEVER fabricate confidence values
- ❌ NEVER hard-code fake AI results into production logic
- ❌ NEVER claim food is "safe to eat" or "definitely unsafe"
- ✅ If the model is unavailable, use a clearly labeled development/mock mode
- ✅ Always include `model_version` in every prediction response
- ✅ Always include a food-safety disclaimer

### Development/Mock Mode
- Must be explicitly labeled in UI and API responses
- Must use `model_version: "dev-heuristic-v0.1"` (not "v1.0")
- Must display a visible banner in the frontend
- Must be documented in PROJECT_CONTEXT.md

### Confidence Handling
- Derive thresholds from model evaluation — never pre-define arbitrary values
- Low confidence → warn user, suggest re-upload
- Never display 100% confidence

### Out-of-Distribution
- Reject non-food images
- Reject unsupported food categories
- Reject extremely poor quality images
- Return helpful guidance, not a fake prediction

---

## 6. Testing Rules

- Every feature must have tests before being marked complete
- Tests must be automated and repeatable
- Test both happy paths and error paths
- Never claim tests passed if they were not actually run
- Backend: pytest with ≥70% coverage target
- Frontend: Vitest for component and hook tests

---

## 7. Documentation Rules

- Update documentation when changing functionality
- Keep README.md current with setup instructions
- Update CHANGELOG.md for every significant change
- Update PROJECT_CONTEXT.md after major decisions
- API changes must be reflected in API.md

---

## 8. Git Rules

- Write clear, descriptive commit messages
- Never commit secrets, credentials, or `.env` files
- Never commit large binary files (model weights, datasets)
- Use `.gitignore` properly
