# Government Scheme Finder
### Multilingual, Voice-First Citizen Benefits Discovery Platform
**Full-Stack Application: Python Flask REST API + SQLite Database + HTML5/CSS3/Vanilla JS Frontend**

---

## 1. Project Overview
**Government Scheme Finder** is a citizen entitlement discovery service that empowers Indian citizens to identify relevant welfare programs in **English**, **తెలుగు (Telugu)**, and **हिंदी (Hindi)**.

The platform combines a voice-enabled frontend interface with a Python Flask REST API and SQLite database that evaluates eligibility parameters (age, occupation, income bracket, state domicile, and inclusion factors) without requiring Aadhaar numbers or confidential personal credentials.

---

## 2. Project Directory Structure

```
government-scheme-finder/
├── backend/
│   ├── __init__.py          # Backend package initializer
│   ├── app.py               # Flask application factory, CORS, static serving & error handlers
│   ├── config.py            # Central configuration (DB path, ports, disclaimers)
│   ├── database.py          # SQLite connection manager, schema initialization & safe queries
│   ├── seed_data.py         # Authentic public government scheme dataset (12 verified programs)
│   ├── test_api.py          # Automated test suite for endpoints and database
│   └── routes/
│       ├── __init__.py      # Routes package initializer
│       └── schemes.py       # REST API endpoints (GET, GET /<id>, POST /search)
│
├── frontend/                # Complete Frontend (Untouched & 100% Preserved)
│   ├── index.html           # Accessible, semantic UI with custom SVG graphics
│   ├── style.css            # Fintech-grade CSS design system & accessibility tokens
│   └── script.js            # Trilingual i18n, Web Speech APIs & resilient API client
│
├── requirements.txt         # Python dependencies
├── run.py                   # Single-command launcher for backend & frontend
└── README.md                # Documentation and run instructions
```

---

## 3. Technology Stack

- **Backend**: Python 3.10+ & Flask 3.1+
- **Database**: SQLite3 (thread-safe with row factory)
- **API Protocol**: RESTful JSON API with HTTP status codes and CORS headers
- **Frontend**: HTML5, Modern CSS3, Vanilla JavaScript (ES6+)
- **Speech APIs**: Native Web Speech API (`SpeechRecognition` & `SpeechSynthesis`)

---

## 4. SQLite Database Schema

The database is stored in `backend/schemes.db` and initialized automatically on first startup:

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | TEXT | PRIMARY KEY | Unique slug (e.g., `pm-kisan`, `ayushman-bharat`) |
| `title` | TEXT | NOT NULL | Official scheme name |
| `acronym` | TEXT | NOT NULL | Commonly recognized acronym |
| `department` | TEXT | NOT NULL | Ministry or nodal government agency |
| `category` | TEXT | NOT NULL | `agriculture`, `education`, `health`, `business`, `women`, `social` |
| `scope` | TEXT | NOT NULL | Geographic scope (e.g., `Central (All States)`, `Telangana & Andhra Pradesh`) |
| `benefit` | TEXT | NOT NULL | Benefit entitlement summary (e.g., `₹6,000 / Year DBT`) |
| `benefit_value` | INTEGER | NOT NULL | Numeric benefit magnitude used for sorting |
| `description` | TEXT | NOT NULL | Plain-language overview of the scheme |
| `min_age` | INTEGER | NOT NULL | Minimum eligible age |
| `max_age` | INTEGER | NOT NULL | Maximum eligible age |
| `gender` | TEXT | NOT NULL | `all`, `female`, `male` |
| `income_max` | INTEGER | NOT NULL | Annual family income ceiling in INR |
| `occupations` | TEXT | NOT NULL | JSON array of eligible occupations |
| `states` | TEXT | NOT NULL | JSON array of eligible states or `["all"]` |
| `requires_land` | INTEGER | NOT NULL | `1` if cultivable landholding required, else `0` |
| `requires_girl_child` | INTEGER | NOT NULL | `1` if girl child under 10 required, else `0` |
| `requires_bpl` | INTEGER | NOT NULL | `1` if Ration/BPL card required, else `0` |
| `criteria_summary` | TEXT | - | Plain-language criteria summary |
| `documents` | TEXT | NOT NULL | JSON array of required documents |
| `application_steps` | TEXT | NOT NULL | JSON array of `{step, text}` instructions |
| `official_url` | TEXT | NOT NULL | Verified `.gov.in` / `.nic.in` portal link |
| `verification_status` | TEXT | NOT NULL | Verification label (e.g. `Verified Public Scheme Record`) |
| `source_dept` | TEXT | - | Official attribution source |
| `created_at` | TIMESTAMP | DEFAULT | Record creation timestamp |

---

## 5. REST API Documentation

### 5.1 `GET /api/schemes`
Returns all schemes in the catalog with optional query filters.

**Query Parameters:**
- `category` *(optional)*: Filter by category (`agriculture`, `education`, `health`, `business`, `women`, `social`).
- `state` *(optional)*: Filter by state (e.g., `Telangana`, `Andhra Pradesh`, `Maharashtra`).
- `search` or `q` *(optional)*: Keyword search across title, department, benefit, and description.
- `sort` *(optional)*: Sort order (`relevance`, `amount`, `name`).

**Example Response (`200 OK`):**
```json
{
  "status": "success",
  "count": 12,
  "data": [
    {
      "id": "pm-kisan",
      "title": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
      "acronym": "PM-KISAN",
      "department": "Ministry of Agriculture & Farmers Welfare",
      "category": "agriculture",
      "scope": "Central (All States)",
      "benefit": "₹6,000 / Year (₹2,000 in 3 installments)",
      "benefit_value": 6000,
      "criteria": {
        "minAge": 18,
        "maxAge": 100,
        "incomeMax": 2000000,
        "occupations": ["farmer"],
        "states": ["all"]
      },
      "officialUrl": "https://pmkisan.gov.in/",
      "verificationStatus": "Verified Public Scheme Record (Official Portal Available)"
    }
  ],
  "disclaimer": "Preliminary eligibility match only..."
}
```

---

### 5.2 `GET /api/schemes/<id>`
Retrieves full details for a single scheme by its unique identifier.

**Example Request:**
```
GET /api/schemes/ayushman-bharat
```

**Example Response (`200 OK`):**
```json
{
  "status": "success",
  "data": {
    "id": "ayushman-bharat",
    "title": "Ayushman Bharat PM-JAY (Pradhan Mantri Jan Arogya Yojana)",
    "department": "National Health Authority (NHA) / Ministry of Health",
    "benefit": "₹5,00,000 Free Health Cover per Family per Year",
    "documents": [
      "Aadhaar Card or Valid Government Photo ID",
      "Ration Card / BPL Card / Family ID",
      "Active Mobile Number"
    ],
    "application_steps": [
      {"step": "Check SECC / Ration Card Eligibility", "text": "Visit beneficiary.nha.gov.in and verify mobile number."},
      {"step": "e-KYC Verification", "text": "Authenticate via Aadhaar OTP at nearest CSC."},
      {"step": "Download Ayushman PVC Card", "text": "Generate digital Ayushman Card."}
    ],
    "officialUrl": "https://pmjay.gov.in/"
  }
}
```

**Error Response (`404 Not Found`):**
```json
{
  "status": "error",
  "message": "Scheme not found with ID 'unknown-id'."
}
```

---

### 5.3 `POST /api/schemes/search`
Accepts a user demographic profile and calculates compatibility scores (0–100%) against all scheme parameters.

**Request Headers:**
`Content-Type: application/json`

**Request Body:**
```json
{
  "age": 28,
  "gender": "male",
  "state": "Telangana",
  "occupation": "farmer",
  "income": 120000,
  "land": "marginal",
  "category": "OBC",
  "girl_child": false,
  "bpl": true
}
```

**Input Validation Rules:**
- `age`: Must be an integer between 0 and 120.
- `income`: Must be a non-negative number.
- Returns `400 Bad Request` with an array of descriptive validation errors if constraints fail.

**Example Response (`200 OK`):**
```json
{
  "status": "success",
  "count": 12,
  "user_profile": {
    "age": 28,
    "occupation": "farmer",
    "state": "Telangana",
    "income": 120000
  },
  "results": [
    {
      "id": "pm-kisan",
      "title": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
      "match_score": 99,
      "match_label": "High Potential Match",
      "rule_breakdown": {
        "age": {
          "parameter": "Age Limit",
          "requirement": "18 to 100 years",
          "user_value": "28 years",
          "status": "matched",
          "detail": "Age 28 falls within 18 - 100 years."
        },
        "occupation": {
          "parameter": "Occupation",
          "requirement": "Farmer",
          "user_value": "Farmer",
          "status": "matched",
          "detail": "Matches primary occupation: Farmer"
        },
        "income": {
          "parameter": "Family Income Cap",
          "requirement": "Up to ₹2,000,000 / year",
          "user_value": "₹120,000 / year",
          "status": "matched",
          "detail": "Annual income ₹120,000 is within maximum cap ₹2,000,000."
        },
        "state": {
          "parameter": "State Domicile",
          "requirement": "all",
          "user_value": "Telangana",
          "status": "matched",
          "detail": "Available in Central (All States)."
        }
      }
    }
  ],
  "disclaimer": "Preliminary eligibility match only. Final approval and disbursement are determined exclusively by the respective government authority."
}
```

---

## 6. Pan-India Scheme Repository & Data Importer

The database has been expanded to cover genuine welfare initiatives across India, covering the Central Government, all **28 States**, and all **8 Union Territories**.

### 6.1 Database Scale & Statistics
- **Total Unique Stored Schemes**: 59 genuine government schemes
- **Central Programs (Pan-India)**: 16 flagship schemes
- **State Government Programs**: 34 state-specific schemes (covering all 28 States)
- **Union Territory Programs**: 9 UT-specific schemes (covering all 8 Union Territories)
- **Verification Classifications**: 58 "Verified from official source", 1 "Verified State Scheme Record"
- **Coverage**: 100% of Indian States and Union Territories with official portal URLs (`.gov.in` / `.nic.in`)

### 6.2 Data Ingestion & CLI Pipeline
The project includes a robust, idempotent import pipeline in `backend/importer.py` and CLI utility `import_schemes.py`:

```powershell
# Show live database distribution statistics
python import_schemes.py --stats

# Export entire database to JSON
python import_schemes.py --export-json backend/data/exported_schemes.json

# Import new or updated schemes from JSON/CSV with duplicate protection
python import_schemes.py --file backend/data/expanded_schemes.json
python import_schemes.py --file backend/data/expanded_schemes.csv
```

### 6.3 Advanced REST API Endpoints
- `GET /api/schemes?page=1&limit=12&category=all&state=all&level=all&search=...` - Paginated scheme catalog with live `total_count` and `total_pages`.
- `GET /api/schemes/stats` - Live distribution breakdown across 28 states, 8 UTs, categories, levels, and verification status.
- `GET /api/schemes/<id>` - Single scheme lookup with full eligibility requirements, documents, and official URLs.
- `POST /api/schemes/search` - Multi-criteria rule evaluation engine calculating match percentages and rule breakdowns.

---

## 7. How to Install & Run

### Step 1: Open Terminal in Project Directory
```powershell
cd C:\Users\prave\.gemini\antigravity\scratch\government-scheme-finder
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Run the Application
```powershell
python run.py
```

The launcher will initialize the SQLite database (`backend/schemes.db`), verify the 59 authentic schemes, and launch the server:
- **Interactive Web UI**: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
- **Schemes API**: [http://127.0.0.1:5000/api/schemes](http://127.0.0.1:5000/api/schemes)
- **Live Statistics API**: [http://127.0.0.1:5000/api/schemes/stats](http://127.0.0.1:5000/api/schemes/stats)
- **API Health**: [http://127.0.0.1:5000/api/health](http://127.0.0.1:5000/api/health)

---

## 8. Running the Automated Test Suites

### Run Full System & Ingestion Test Suite:
```powershell
python -m backend.test_import_and_search
```
All 9 automated verification tests validate malformed record rejection, JSON/CSV ingest, duplicate detection, state/UT search, category filters, pagination, and 28-state + 8-UT statistics.

### Run Endpoint API Test Suite:
```powershell
python backend/test_api.py
```

Expected output:
```
--- 1. Testing GET /api/health ---
Status: 200

--- 2. Testing GET /api/schemes ---
Status: 200
Count: 12

--- 3. Testing GET /api/schemes?category=agriculture ---
Status: 200
Agri Schemes Count: 3

--- 4. Testing GET /api/schemes/pm-kisan ---
Status: 200

--- 5. Testing GET /api/schemes/invalid-id (404 expected) ---
Status: 404

--- 6. Testing POST /api/schemes/search (Farmer in Telangana) ---
Status: 200
Top Match: PM-KISAN / APY (High Potential Match)

--- 7. Testing POST /api/schemes/search with invalid age (400 expected) ---
Status: 400

 [PASS] ALL BACKEND & DATABASE TESTS PASSED SUCCESSFULLY!
```

---

## 8. Frontend-Backend Compatibility & Resilience

1. **Automatic Discovery**: When the app is served via Flask (`http://127.0.0.1:5000/`), the frontend communicates with the `/api` endpoints automatically.
2. **Resilient Local Fallback**: If the backend is temporarily offline (e.g., when the frontend is opened directly as `file://` or via a separate static server), the frontend seamlessly falls back to its local demonstration data without throwing unhandled exceptions or breaking voice input, stepper navigation, or translation features.
3. **Connection Status Pill**: The catalog displays `REST API Connected • SQLite Database` when the backend is active.

---

## 9. Public Advisory & Compliance Notice

> **Important**: This platform serves strictly as an informational discovery tool. Final eligibility, biometric authentication, and financial disbursements are determined exclusively by the respective Central Ministry, State Government Department, or designated nodal bank. SchemeFinder does not grant official approvals, issue sanctions, or request Aadhaar numbers, biometric keys, or confidential passwords.
