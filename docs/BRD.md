# Business Requirements Document (BRD)

## AI Food Freshness Checker

| Field | Value |
|-------|-------|
| **Document Version** | 1.0 |
| **Status** | DRAFT — Awaiting Approval |
| **Created** | 2026-08-23 |
| **Last Updated** | 2026-08-23 |

---

## Table of Contents

1. [Project Information](#1-project-information)
2. [Business Requirements](#2-business-requirements)
3. [Target Users](#3-target-users)
4. [User Needs](#4-user-needs)
5. [Core Features](#5-core-features)
6. [Functional Requirements](#6-functional-requirements)
7. [Non-Functional Requirements](#7-non-functional-requirements)
8. [Inputs](#8-inputs)
9. [Outputs](#9-outputs)
10. [Business Rules](#10-business-rules)
11. [Security & Privacy](#11-security--privacy)
12. [Risks](#12-risks)
13. [Assumptions](#13-assumptions)
14. [Acceptance Criteria](#14-acceptance-criteria)
15. [Glossary](#15-glossary)
16. [Revision History](#16-revision-history)

---

## 1. Project Information

### 1.1 Project Name

**AI Food Freshness Checker**

### 1.2 Product Vision

Build an AI-powered web application that enables users to capture or upload an image of food and receive a **visual estimate** of its freshness condition — empowering individuals and households to reduce food waste through informed decisions, while clearly communicating that results are visual AI estimates and NOT laboratory food-safety tests.

### 1.3 Project Purpose

Provide an accessible, easy-to-use tool that helps everyday consumers make faster, more informed visual judgements about the freshness of common fruits and vegetables using computer vision and deep learning.

### 1.4 Problem Statement

Consumers frequently discard edible food due to uncertainty about freshness, or conversely consume food that shows visible signs of spoilage because they lack the knowledge to identify them. There is no widely available, consumer-friendly tool that leverages AI to help users visually assess food freshness quickly and conveniently.

### 1.5 Proposed Solution

A responsive web application where users can:

1. Upload or capture a photo of a supported food item.
2. Receive an AI-generated visual freshness classification (FRESH, AGING, or HIGH VISIBLE SPOILAGE RISK).
3. View the confidence level of the prediction.
4. See which visual characteristics influenced the classification.
5. Read a contextual recommendation and mandatory food-safety disclaimer.
6. Review their past analysis history via a personal dashboard.

The AI model uses transfer learning on MobileNetV3 to classify freshness based on visual features. The system explicitly communicates its limitations and never claims to guarantee food safety.

---

## 2. Business Requirements

### 2.1 Business Goals

| ID | Goal |
|----|------|
| BG-001 | Deliver an MVP that demonstrates viable AI-powered food freshness estimation |
| BG-002 | Reduce consumer food waste by providing actionable visual freshness information |
| BG-003 | Establish a responsible AI product that communicates limitations transparently |
| BG-004 | Build a scalable platform that can be extended with additional food categories, multimodal inputs, and advanced analytics |

### 2.2 Objectives

| ID | Objective | Measurable Target |
|----|-----------|-------------------|
| OBJ-001 | Launch a functional MVP supporting 8 food categories | 8 categories classified at ≥80% F1 score |
| OBJ-002 | Achieve reliable freshness classification across 3 classes | Recall ≥85% for HIGH VISIBLE SPOILAGE RISK class |
| OBJ-003 | Deliver sub-5-second end-to-end analysis time | 95th percentile latency ≤5 seconds |
| OBJ-004 | Achieve positive user experience | ≥80% of test users complete the primary flow without assistance |
| OBJ-005 | Ensure responsible AI communication | 100% of results include a food-safety disclaimer |

### 2.3 Expected Outcomes

- Users can visually assess food freshness using their phone or computer camera.
- Users gain awareness of visual spoilage indicators they may not have known.
- Users make more informed keep-or-discard decisions.
- The platform provides a foundation for future food-waste reduction features.

### 2.4 Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| ML model F1 score (weighted) | ≥0.80 | Model evaluation on held-out test set |
| Spoilage class recall | ≥0.85 | Confusion matrix analysis |
| End-to-end latency (p95) | ≤5 seconds | Server-side timing instrumentation |
| Image validation accuracy | ≥95% rejection of non-food images | Validation test suite |
| User task completion rate | ≥80% | Usability testing sessions |
| Uptime | ≥99% | Monitoring infrastructure |

---

## 3. Target Users

### 3.1 Persona: Home Consumer — "Maya"

| Attribute | Detail |
|-----------|--------|
| **Age** | 25–45 |
| **Tech Comfort** | Moderate — uses smartphone apps daily |
| **Goal** | Quickly check if food in her fridge is still good before cooking or discarding |
| **Pain Point** | Unsure whether a slightly soft tomato is still usable; often throws away food "just in case" |
| **Behavior** | Wants a fast answer — upload a photo and get a result in seconds |
| **Device** | Primarily mobile phone, occasionally laptop |

### 3.2 Persona: Health-Conscious Individual — "Raj"

| Attribute | Detail |
|-----------|--------|
| **Age** | 20–35 |
| **Tech Comfort** | High — early adopter of health/wellness apps |
| **Goal** | Track food freshness as part of a broader health-conscious lifestyle |
| **Pain Point** | Wants to avoid consuming visually degraded food but lacks expert knowledge |
| **Behavior** | Would check food regularly; interested in history and trends |
| **Device** | Smartphone |

### 3.3 Persona: Budget-Conscious Shopper — "Elena"

| Attribute | Detail |
|-----------|--------|
| **Age** | 30–55 |
| **Tech Comfort** | Low to moderate |
| **Goal** | Reduce food waste to save money |
| **Pain Point** | Buys in bulk; some items spoil before she can use them |
| **Behavior** | Wants simple, clear recommendations — not technical jargon |
| **Device** | Smartphone, tablet |

---

## 4. User Needs

| ID | User Need | Priority |
|----|-----------|----------|
| UN-001 | I need to quickly check if my food looks fresh by taking a photo | **Must Have** |
| UN-002 | I need to understand WHY the AI thinks my food is aging or spoiled | **Must Have** |
| UN-003 | I need a clear recommendation on what to do with the food | **Must Have** |
| UN-004 | I need to know that this is an estimate, not a safety guarantee | **Must Have** |
| UN-005 | I need to see my past checks so I can track patterns | **Should Have** |
| UN-006 | I need the app to work well on my phone | **Must Have** |
| UN-007 | I need the app to be fast — I don't want to wait more than a few seconds | **Must Have** |
| UN-008 | I need the app to tell me when it can't identify my food, rather than guessing | **Must Have** |
| UN-009 | I need a simple, uncluttered interface that I can use without instructions | **Must Have** |
| UN-010 | I need my data to be private and secure | **Must Have** |

---

## 5. Core Features

### 5.1 MVP Features

| ID | Feature | Priority | Phase |
|----|---------|----------|-------|
| CF-001 | Image Upload | Must Have | MVP |
| CF-002 | Camera Capture | Must Have | MVP |
| CF-003 | Image Validation | Must Have | MVP |
| CF-004 | Food Identification | Must Have | MVP |
| CF-005 | Freshness Classification | Must Have | MVP |
| CF-006 | Confidence Score | Must Have | MVP |
| CF-007 | Visual Explanation (observed indicators) | Must Have | MVP |
| CF-008 | Recommendation Engine | Must Have | MVP |
| CF-009 | Food-Safety Disclaimer | Must Have | MVP |
| CF-010 | User Registration & Authentication | Must Have | MVP |
| CF-011 | Analysis History | Should Have | MVP |
| CF-012 | Basic Dashboard | Should Have | MVP |

### 5.2 Future Features (NOT in MVP)

| ID | Feature | Priority | Phase |
|----|---------|----------|-------|
| FF-001 | Grad-CAM Explainability Heatmap | High | Post-MVP |
| FF-002 | Food Inventory Tracking | Medium | Post-MVP |
| FF-003 | Expiration/Freshness Notifications | Medium | Post-MVP |
| FF-004 | Storage Condition Tracking | Medium | Post-MVP |
| FF-005 | Waste Analytics Dashboard | Medium | Post-MVP |
| FF-006 | Recipe Suggestions (based on freshness) | Low | Post-MVP |
| FF-007 | Multimodal Analysis (date, temp, humidity) | Low | Post-MVP |
| FF-008 | Advanced Models (EfficientNet, ensemble) | Medium | Post-MVP |
| FF-009 | Native Mobile Applications | Low | Post-MVP |
| FF-010 | Multi-language Support | Low | Post-MVP |

> [!WARNING]
> Future features MUST NOT be implemented until their phase is explicitly approved. Do not scope-creep into future features during MVP development.

---

## 6. Functional Requirements

### 6.1 Image Upload — CF-001

| ID | Requirement |
|----|-------------|
| FR-001 | The system SHALL allow users to upload an image file from their device |
| FR-002 | The system SHALL accept JPEG and PNG image formats |
| FR-003 | The system SHALL reject files exceeding 10 MB |
| FR-004 | The system SHALL reject non-image file types with a descriptive error |
| FR-005 | The system SHALL display a preview of the uploaded image before analysis |
| FR-006 | The system SHALL support drag-and-drop upload on desktop browsers |

### 6.2 Camera Capture — CF-002

| ID | Requirement |
|----|-------------|
| FR-007 | The system SHALL provide a camera capture option using the browser's MediaDevices API |
| FR-008 | The system SHALL request camera permission with a clear explanation |
| FR-009 | The system SHALL gracefully handle denied camera permissions with fallback to upload |
| FR-010 | The system SHALL capture a still image from the camera stream |
| FR-011 | The system SHALL display a preview of the captured image before analysis |

### 6.3 Image Validation — CF-003

| ID | Requirement |
|----|-------------|
| FR-012 | The system SHALL validate image dimensions (minimum 224×224 pixels) |
| FR-013 | The system SHALL validate image file integrity (not corrupted) |
| FR-014 | The system SHALL reject images that are predominantly blank, fully black, or fully white |
| FR-015 | The system SHALL provide specific, user-friendly error messages for each validation failure |
| FR-016 | The system SHALL perform server-side validation in addition to client-side validation |

### 6.4 Food Identification — CF-004

| ID | Requirement |
|----|-------------|
| FR-017 | The system SHALL identify whether the uploaded image contains a supported food item |
| FR-018 | The system SHALL support the following 8 food categories: Apple, Banana, Tomato, Potato, Orange, Carrot, Cucumber, Strawberry |
| FR-019 | The system SHALL reject non-food images with the message: "Unable to identify a supported food item. Please upload a clear image of one supported food." |
| FR-020 | The system SHALL reject images of unsupported food items with a similar message |
| FR-021 | The system SHALL handle images containing multiple food items by informing the user to submit one food at a time |

### 6.5 Freshness Classification — CF-005

| ID | Requirement |
|----|-------------|
| FR-022 | The system SHALL classify each supported food into exactly one of three freshness classes: FRESH, AGING, HIGH VISIBLE SPOILAGE RISK |
| FR-023 | The system SHALL use a trained deep learning model (MobileNetV3 via transfer learning) for classification |
| FR-024 | The system SHALL NOT hard-code or fabricate freshness predictions |
| FR-025 | If the model is unavailable, the system SHALL return an error rather than a fake result |

### 6.6 Confidence Score — CF-006

| ID | Requirement |
|----|-------------|
| FR-026 | The system SHALL return a confidence percentage (0–100%) for each prediction |
| FR-027 | The system SHALL derive confidence from the model's softmax output — never fabricated |
| FR-028 | The system SHALL categorize confidence into tiers (High / Medium / Low) based on thresholds determined during model evaluation |
| FR-029 | For LOW confidence predictions, the system SHALL display a warning: "This result has low confidence. Consider uploading a clearer image." |

### 6.7 Visual Explanation — CF-007

| ID | Requirement |
|----|-------------|
| FR-030 | The system SHALL display a list of observed visual indicators that influenced the prediction (e.g., "Dark spots", "Wrinkled surface", "Discoloration") |
| FR-031 | Visual indicators SHALL be specific to the food category and freshness class |
| FR-032 | The system SHALL NOT present indicators as definitive proof of spoilage |
| FR-033 | Indicators SHALL be phrased as observations (e.g., "Visible dark spots detected") rather than conclusions |

### 6.8 Recommendation Engine — CF-008

| ID | Requirement |
|----|-------------|
| FR-034 | The system SHALL provide a contextual recommendation based on the freshness classification |
| FR-035 | FRESH recommendation example: "No obvious visual spoilage detected. Store properly to maintain freshness." |
| FR-036 | AGING recommendation example: "Visible signs suggest this food may be aging. Consider using soon and inspect carefully before consumption." |
| FR-037 | HIGH VISIBLE SPOILAGE RISK recommendation example: "Visible indicators suggest significant degradation. Exercise caution and inspect thoroughly. When in doubt, discard." |
| FR-038 | Recommendations SHALL NEVER state that food is "safe to eat" or "definitely spoiled" |

### 6.9 Food-Safety Disclaimer — CF-009

| ID | Requirement |
|----|-------------|
| FR-039 | The system SHALL display a food-safety disclaimer on EVERY analysis result |
| FR-040 | The disclaimer SHALL include text similar to: "This is a visual AI estimate only. It is not a laboratory food-safety test. Visual analysis cannot detect bacteria, toxins, or internal spoilage. Always use your own judgement and follow food-safety guidelines." |
| FR-041 | The disclaimer SHALL be visually prominent and not collapsible on the result view |
| FR-042 | The system SHALL include a disclaimer link or notice on the landing page |

### 6.10 User Registration & Authentication — CF-010

| ID | Requirement |
|----|-------------|
| FR-043 | The system SHALL allow users to register with email and password |
| FR-044 | The system SHALL validate email format and password strength (minimum 8 characters, at least one letter and one number) |
| FR-045 | The system SHALL authenticate users via JWT tokens |
| FR-046 | The system SHALL provide login and logout functionality |
| FR-047 | The system SHALL protect history and dashboard endpoints with authentication |
| FR-048 | **[ASSUMPTION A-002]** The system SHALL allow guest/anonymous access to the core analysis feature (upload → analyze → result) without requiring login |
| FR-049 | Guest analyses SHALL NOT be persisted to history |

### 6.11 Analysis History — CF-011

| ID | Requirement |
|----|-------------|
| FR-050 | The system SHALL store each analysis performed by an authenticated user |
| FR-051 | The system SHALL display a paginated list of past analyses |
| FR-052 | Each history entry SHALL show: food category, freshness class, confidence, date/time, and thumbnail |
| FR-053 | The user SHALL be able to view the full details of a past analysis |
| FR-054 | The user SHALL be able to delete individual history entries |
| FR-055 | The system SHALL show only the authenticated user's own history (never another user's) |

### 6.12 Basic Dashboard — CF-012

| ID | Requirement |
|----|-------------|
| FR-056 | The system SHALL display a basic dashboard for authenticated users |
| FR-057 | The dashboard SHALL show: total scans performed, freshness distribution (pie/donut chart), most-scanned food categories, and recent activity feed |
| FR-058 | The dashboard SHALL update when a new analysis is completed |
| FR-059 | The dashboard SHALL render correctly on mobile and desktop viewports |

---

## 7. Non-Functional Requirements

### 7.1 Performance

| ID | Requirement |
|----|-------------|
| NFR-001 | End-to-end analysis latency (upload → result) SHALL be ≤5 seconds at the 95th percentile |
| NFR-002 | ML inference time SHALL be ≤2 seconds per image |
| NFR-003 | Frontend initial page load SHALL complete within 3 seconds on a 4G connection |
| NFR-004 | API response time for non-ML endpoints SHALL be ≤500ms at the 95th percentile |

### 7.2 Scalability

| ID | Requirement |
|----|-------------|
| NFR-005 | The architecture SHALL support horizontal scaling of the backend API |
| NFR-006 | The ML inference component SHALL be separable from the API server for independent scaling in future phases |
| NFR-007 | The database SHALL handle at least 10,000 analysis records per user without performance degradation |

### 7.3 Reliability

| ID | Requirement |
|----|-------------|
| NFR-008 | The system SHALL maintain ≥99% uptime during operational hours |
| NFR-009 | The system SHALL handle ML model loading failures gracefully (return error, not crash) |
| NFR-010 | The system SHALL implement database connection pooling |

### 7.4 Maintainability

| ID | Requirement |
|----|-------------|
| NFR-011 | Code SHALL follow clean-code principles: small functions, meaningful names, separation of concerns |
| NFR-012 | The ML pipeline SHALL be decoupled from business logic |
| NFR-013 | The codebase SHALL have ≥70% test coverage for backend logic |
| NFR-014 | All public APIs SHALL be documented |

### 7.5 Security

| ID | Requirement |
|----|-------------|
| NFR-015 | All API communication SHALL use HTTPS in production |
| NFR-016 | Passwords SHALL be hashed using bcrypt or argon2 |
| NFR-017 | JWT tokens SHALL have a reasonable expiration time (e.g., 24 hours) |
| NFR-018 | File uploads SHALL be validated for type, size, and content |
| NFR-019 | All user inputs SHALL be sanitized to prevent injection attacks |
| NFR-020 | No secrets, API keys, or credentials SHALL be hard-coded in source code |
| NFR-021 | Rate limiting SHALL be implemented on authentication and analysis endpoints |

### 7.6 Accessibility

| ID | Requirement |
|----|-------------|
| NFR-022 | The UI SHALL meet WCAG 2.1 Level AA accessibility standards |
| NFR-023 | All images and icons SHALL have appropriate alt text |
| NFR-024 | The UI SHALL be navigable via keyboard |
| NFR-025 | Color SHALL not be the sole means of conveying information (e.g., freshness indicators SHALL also use text labels and icons) |

### 7.7 Usability

| ID | Requirement |
|----|-------------|
| NFR-026 | A new user SHALL be able to complete the primary flow (upload → result) without instructions |
| NFR-027 | Loading states SHALL be displayed during image upload and analysis |
| NFR-028 | Error messages SHALL be user-friendly and actionable |
| NFR-029 | The UI SHALL be responsive across mobile (≥320px), tablet (≥768px), and desktop (≥1024px) viewports |

### 7.8 Availability

| ID | Requirement |
|----|-------------|
| NFR-030 | The system SHALL be available 24/7 with planned maintenance windows communicated in advance |
| NFR-031 | The system SHALL implement health-check endpoints for monitoring |

---

## 8. Inputs

| Input | Source | Format | Constraints |
|-------|--------|--------|-------------|
| Food image (upload) | User device file system | JPEG, PNG | ≤10 MB, min 224×224 px |
| Food image (camera) | Browser camera API | JPEG (captured frame) | Min 224×224 px |
| User credentials | Registration/login form | Email + password | Valid email; password ≥8 chars, ≥1 letter, ≥1 number |
| Optional food metadata | Future phase — not MVP | JSON | N/A for MVP |
| Optional storage info | Future phase — not MVP | JSON | N/A for MVP |

---

## 9. Outputs

| Output | Description | Format |
|--------|-------------|--------|
| Food category | Identified food name | String (e.g., "Tomato") |
| Freshness classification | One of: FRESH, AGING, HIGH VISIBLE SPOILAGE RISK | Enum string |
| Confidence score | Model prediction confidence | Float 0.0–1.0 (displayed as percentage) |
| Visual indicators | List of observed visual characteristics | Array of strings |
| Recommendation | Contextual guidance based on freshness class | String |
| Safety notice | Food-safety disclaimer | String (always included) |
| Model version | Version identifier of the ML model used | String |
| Analysis metadata | Timestamp, analysis ID | ISO 8601 timestamp, UUID |

---

## 10. Business Rules

| ID | Rule | Rationale |
|----|------|-----------|
| BR-001 | Unsupported food items SHALL NOT receive a freshness prediction. The system SHALL return a clear "unsupported food" message. | Prevents fabricated/unreliable predictions |
| BR-002 | Images that fail quality validation (corrupted, too small, blank, etc.) SHALL be rejected with a specific error message. | Ensures minimum input quality for reliable predictions |
| BR-003 | LOW confidence predictions SHALL include an explicit warning and suggestion to re-upload a clearer image. | Manages user expectations; prevents over-reliance on uncertain results |
| BR-004 | The system SHALL NEVER state or imply that food is "safe to eat" or "definitely unsafe." | Legal liability; AI cannot guarantee food safety |
| BR-005 | All results SHALL include the food-safety disclaimer. No mechanism SHALL allow users to permanently dismiss it on the result view. | Responsible AI communication |
| BR-006 | Unknown or unrecognized conditions SHALL trigger a fallback response: "Unable to analyze this image. Please try a different photo." | Graceful degradation |
| BR-007 | Non-food images SHALL be rejected, not classified. | Prevents nonsensical predictions |
| BR-008 | Multiple foods in one image SHALL trigger a message asking the user to photograph one item at a time. | Model is trained on single-food images |
| BR-009 | If the ML model service is unavailable, the API SHALL return a 503 Service Unavailable error, NOT a fabricated result. | System integrity; never fake AI predictions |
| BR-010 | Guest users (unauthenticated) MAY use the core analysis feature. History and dashboard require authentication. | Reduces friction for first-time users |
| BR-011 | Users SHALL only access their own data. Cross-user data access SHALL be prevented at the API and database levels. | Data privacy and multi-user isolation |
| BR-012 | Images uploaded by users SHALL be retained for a maximum of 90 days, after which they SHALL be automatically purged. Users MAY delete their images at any time. | Storage cost management and privacy |

---

## 11. Security & Privacy

### 11.1 Authentication

| Aspect | Specification |
|--------|---------------|
| Method | Email + password registration; JWT-based session tokens |
| Password storage | Hashed with bcrypt (cost factor ≥12) or argon2 |
| Token expiry | Access token: 24 hours; Refresh token: 7 days |
| Brute-force protection | Rate limit login attempts (e.g., 5 failed attempts → 15-minute lockout) |

### 11.2 Authorization

| Aspect | Specification |
|--------|---------------|
| Core analysis | Available to both guests and authenticated users |
| History & Dashboard | Authenticated users only |
| Data isolation | Users can only access their own analysis records |
| Admin access | Not in MVP scope |

### 11.3 Data Protection

| Aspect | Specification |
|--------|---------------|
| Data in transit | HTTPS/TLS 1.2+ enforced in production |
| Data at rest | Database encryption at rest (cloud provider managed) |
| PII stored | Email, hashed password, analysis history. No unnecessary PII collection. |
| Data deletion | Users can delete their account and all associated data |

### 11.4 Image Handling

| Aspect | Specification |
|--------|---------------|
| Upload validation | File type, size, dimensions, content-type header verification |
| Storage | Server-side object storage; images not publicly accessible |
| Access control | Only the owning user can access their uploaded images via authenticated API |
| Retention | 90-day automatic purge (ASSUMPTION — requires approval) |
| Stripping metadata | EXIF data SHALL be stripped from uploaded images before storage to prevent location leakage |

### 11.5 Secret Management

| Aspect | Specification |
|--------|---------------|
| Secrets storage | Environment variables; never in source code |
| Configuration | `.env` files excluded from version control; `.env.example` template provided |
| Production | Cloud-native secret management (e.g., cloud KMS or secrets manager) |

---

## 12. Risks

| ID | Risk | Severity | Likelihood | Mitigation Strategy |
|----|------|----------|------------|---------------------|
| RISK-001 | **False negative**: spoiled food classified as FRESH | 🔴 Critical | Medium | Bias model training toward recall for spoilage class; prominent disclaimers; conservative thresholds |
| RISK-002 | **False positive**: fresh food classified as SPOILED | 🟡 Medium | Medium | May cause unnecessary waste but is safer; monitor and improve model precision |
| RISK-003 | **Dataset bias**: limited food varieties, lighting conditions, or backgrounds in training data | 🟡 Medium | High | Aggressive data augmentation; document known biases; continuous data collection |
| RISK-004 | **User over-reliance**: treating AI estimate as food-safety certification | 🔴 Critical | Medium | Mandatory disclaimers; careful wording; terms of service; never say "safe" |
| RISK-005 | **Poor image quality**: blurry, dark, over-exposed uploads | 🟡 Medium | High | Image quality validation; re-upload prompts; user guidance on good photos |
| RISK-006 | **Multiple foods in image**: model trained on single items | 🟡 Medium | Medium | Detection and user notification to submit one food at a time |
| RISK-007 | **Unseen food types**: users upload food outside the 8 supported categories | 🟡 Medium | High | OOD detection; clear supported-food list in UI; graceful rejection |
| RISK-008 | **Variety differences**: model may not generalize (e.g., green vs red apple) | 🟡 Medium | Medium | Include variety diversity in dataset; document limitations |
| RISK-009 | **Camera quality**: low-resolution phone cameras | 🟢 Low | Medium | Minimum resolution enforcement (224×224); guidance in UI |
| RISK-010 | **Model drift**: real-world distribution shifts over time | 🟡 Medium | Medium | Prediction logging; periodic retraining; monitoring pipeline (future) |
| RISK-011 | **Dataset licensing**: using datasets without proper permissions | 🟡 Medium | Low | Verify every dataset license before use; document in DATASET.md |
| RISK-012 | **Legal liability**: user health consequences from following AI recommendation | 🔴 Critical | Low | Terms of service; disclaimers; never guarantee safety; legal review recommended |
| RISK-013 | **Latency**: slow inference degrading UX | 🟢 Low | Low | MobileNetV3 is lightweight; set performance budgets; optimize preprocessing |
| RISK-014 | **Storage costs**: unbounded growth of stored images | 🟡 Medium | Medium | Retention policy (90 days); compression; size limits |

---

## 13. Assumptions

> [!IMPORTANT]
> These assumptions require explicit approval. They are NOT confirmed requirements.

| ID | Assumption | Status |
|----|-----------|--------|
| A-001 | The MVP is a **web application** (not native mobile). Responsive design covers mobile use. | ⏳ Pending Approval |
| A-002 | Camera capture uses the **browser's MediaDevices API** (getUserMedia). | ⏳ Pending Approval |
| A-003 | **Guest/anonymous access** is permitted for the core analysis feature. Authentication is required only for history and dashboard. | ⏳ Pending Approval |
| A-004 | **Images are stored server-side** (object storage) for authenticated users' history. Guest images are processed but not persisted. | ⏳ Pending Approval |
| A-005 | The application is **single-tenant** — each user sees only their own data. | ⏳ Pending Approval |
| A-006 | **English only** for MVP. | ⏳ Pending Approval |
| A-007 | ML inference runs **server-side** (not on-device). | ⏳ Pending Approval |
| A-008 | **One food item per image** is the primary supported scenario. | ⏳ Pending Approval |
| A-009 | Accepted image formats are **JPEG and PNG**. Maximum file size is **10 MB**. | ⏳ Pending Approval |
| A-010 | Training datasets are sourced from **publicly available datasets** with verified licenses. | ⏳ Pending Approval |
| A-011 | **No payment or subscription system** in the MVP. | ⏳ Pending Approval |
| A-012 | Inference is fast enough for **synchronous API responses** (no job queue for MVP). | ⏳ Pending Approval |
| A-013 | **PostgreSQL** is used for the primary database. | ⏳ Pending Approval |
| A-014 | Image retention policy is **90 days** with user-initiated deletion available. | ⏳ Pending Approval |
| A-015 | Deployment target is a **cloud-agnostic Docker-based setup**. | ⏳ Pending Approval |
| A-016 | Dashboard shows: total scans, freshness distribution, most-scanned categories, recent activity. | ⏳ Pending Approval |
| A-017 | ML model is embedded in the FastAPI process for MVP; separate model serving is a future optimization. | ⏳ Pending Approval |

---

## 14. Acceptance Criteria

### AC-001: Image Upload

- [ ] User can select a JPEG or PNG file from their device.
- [ ] Files exceeding 10 MB are rejected with a clear error message.
- [ ] Non-image files are rejected with a descriptive error.
- [ ] A preview of the selected image is displayed before analysis.
- [ ] Drag-and-drop upload works on desktop browsers.

### AC-002: Camera Capture

- [ ] Camera permission dialog is presented with a clear explanation.
- [ ] User can capture a still image from the live camera feed.
- [ ] Denied camera permission falls back to the upload option gracefully.
- [ ] Captured image preview is shown before analysis.

### AC-003: Image Validation

- [ ] Images below 224×224 pixels are rejected with an error.
- [ ] Corrupted image files are rejected.
- [ ] Blank/black/white images are rejected.
- [ ] All validation errors display user-friendly messages.

### AC-004: Food Identification

- [ ] All 8 supported foods are correctly identified (verified via test set).
- [ ] Non-food images receive: "Unable to identify a supported food item."
- [ ] Unsupported food receives a similar rejection message.
- [ ] Multiple foods trigger: "Please upload an image of a single food item."

### AC-005: Freshness Classification

- [ ] Each analysis returns exactly one of: FRESH, AGING, HIGH VISIBLE SPOILAGE RISK.
- [ ] Classification is generated by the ML model — never hard-coded.
- [ ] When the model is unavailable, the API returns a 503 error.

### AC-006: Confidence Score

- [ ] Confidence is returned as a percentage between 0% and 100%.
- [ ] Confidence is derived from the model — never fabricated.
- [ ] Low-confidence results display a visible warning.

### AC-007: Visual Explanation

- [ ] At least 1–3 visual indicators are listed per analysis result.
- [ ] Indicators are relevant to the specific food and freshness class.
- [ ] Indicators are phrased as observations, not conclusions.

### AC-008: Recommendation

- [ ] Each freshness class has a distinct, appropriate recommendation.
- [ ] No recommendation contains "safe to eat" or "definitely spoiled."
- [ ] Recommendations are actionable and clear.

### AC-009: Food-Safety Disclaimer

- [ ] Every result page displays the food-safety disclaimer.
- [ ] The disclaimer is visible without scrolling on mobile viewports.
- [ ] The disclaimer cannot be permanently dismissed.

### AC-010: Authentication

- [ ] Users can register with email and password.
- [ ] Invalid email/weak password are rejected with specific errors.
- [ ] Users can log in and receive a JWT token.
- [ ] Users can log out (token invalidated client-side).
- [ ] Protected endpoints reject unauthenticated requests with 401.

### AC-011: Analysis History

- [ ] Authenticated users see a paginated list of their past analyses.
- [ ] Each entry shows: food, freshness, confidence, date, thumbnail.
- [ ] Users can view full details of a past analysis.
- [ ] Users can delete individual history entries.
- [ ] Users cannot see another user's history.

### AC-012: Dashboard

- [ ] Dashboard displays: total scans, freshness distribution chart, top categories, recent activity.
- [ ] Dashboard updates after a new analysis.
- [ ] Dashboard renders correctly on mobile and desktop.
- [ ] Dashboard is accessible only to authenticated users.

### AC-013: Out-of-Distribution Handling

- [ ] Non-food images (e.g., laptop, car) are NOT classified as food.
- [ ] The system returns a clear "not supported" message.
- [ ] No confidence score or freshness class is shown for rejected images.

### AC-014: Responsive Design

- [ ] UI renders correctly on viewports: 320px, 768px, 1024px, 1440px.
- [ ] All interactive elements are tap-friendly on mobile.
- [ ] No horizontal scrolling on any supported viewport.

### AC-015: Performance

- [ ] Upload → result completes in ≤5 seconds (p95) on a standard connection.
- [ ] Loading states are displayed during analysis.
- [ ] Initial page load completes in ≤3 seconds on 4G.

### AC-016: Security

- [ ] No secrets in source code or version control.
- [ ] Passwords are stored as bcrypt/argon2 hashes.
- [ ] JWT tokens expire appropriately.
- [ ] Rate limiting is active on login and analysis endpoints.
- [ ] EXIF data is stripped from stored images.

---

## 15. Glossary

| Term | Definition |
|------|-----------|
| **Freshness Classification** | A three-class visual estimate: FRESH, AGING, or HIGH VISIBLE SPOILAGE RISK |
| **Confidence Score** | The probability (0–100%) that the model assigns to its top prediction |
| **Visual Indicators** | Specific visual characteristics observed in the image (e.g., dark spots, wrinkling) |
| **OOD (Out-of-Distribution)** | Input data that falls outside the model's training distribution |
| **Transfer Learning** | A technique where a model pre-trained on a large dataset is fine-tuned on a smaller, task-specific dataset |
| **MobileNetV3** | A lightweight convolutional neural network optimized for mobile and edge devices |
| **Grad-CAM** | Gradient-weighted Class Activation Mapping — a visual explainability technique for CNNs |
| **MVP** | Minimum Viable Product — the first shippable version with core features only |
| **JWT** | JSON Web Token — a standard for securely transmitting authentication claims |
| **False Negative** | A prediction where spoiled food is incorrectly classified as FRESH (high-risk failure) |

---

## 16. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-08-23 | AI Architect | Initial BRD creation |

---

> **Document Status: DRAFT — Awaiting Stakeholder Approval**
>
> This document must be reviewed and approved before proceeding to Phase 2 (Architecture Document).
