# StaffSync

B2B HRMS (Human Resource Management System) built as a monorepo with a
cloud-native mindset: FastAPI backend, React + Vite frontend, MySQL 8,
Docker Compose for local development, pytest against a real database,
and GitHub Actions CI.

> Convention: everything in this repo is in **English** — code, database
> schema, API endpoints, and docs.

---

## 1. Tech stack

| Layer    | Technology                                    |
| -------- | --------------------------------------------- |
| Backend  | Python 3.12, FastAPI, SQLAlchemy 2, Pydantic  |
| Frontend | React 19, React Router 7, Vite 8              |
| Database | MySQL 8.0                                     |
| Testing  | pytest + httpx (`TestClient`), real MySQL     |
| Local    | Docker + Docker Compose                       |
| CI       | GitHub Actions (MySQL 8 service container)    |
| Future   | Kubernetes + Helm (`deploy/`), frontend image |

---

## 2. Repository structure

```text
StaffSync/
├── .github/workflows/ci-backend.yaml  # Backend CI: MySQL service + pytest
├── backend/
│   ├── src/
│   │   ├── main.py                    # FastAPI app, router wiring, /health
│   │   ├── config/database.py         # Engine + SessionLocal + get_db (env vars)
│   │   ├── models/                    # SQLAlchemy models
│   │   │   ├── department.py          # Department (table: departments)
│   │   │   └── employee.py            # Employee (table: employees)
│   │   ├── schemas/                   # Pydantic BaseModel validation
│   │   │   ├── department.py          # DepartmentBase/Create/Update/Response
│   │   │   └── employee.py            # EmployeeBase/Create/Update/Response
│   │   └── routes/                    # APIRouter modules (no single-file routes)
│   │       ├── departments.py         # CRUD /api/departments
│   │       └── employees.py           # CRUD /api/employees
│   ├── tests/                         # pytest suite (MySQL, no SQLite)
│   │   ├── conftest.py                # Test DB setup + TestClient fixture
│   │   ├── test_health.py
│   │   ├── test_departments.py
│   │   └── test_employees.py
│   ├── requirements.txt
│   └── Dockerfile                     # python:3.12-slim + uvicorn --reload
├── frontend/staffsync-frontend/
│   ├── src/
│   │   ├── App.jsx                    # Router: /, /departments, /employees
│   │   ├── main.jsx                   # BrowserRouter + global CSS import
│   │   ├── components/Navbar.jsx      # Top nav + hamburger menu (mobile)
│   │   ├── pages/Home.jsx             # Welcome landing page
│   │   ├── pages/Departments.jsx      # Department cards page
│   │   ├── pages/Employees.jsx        # Employee stats-table page
│   │   └── style/global.css           # Global NBA.com-inspired theme
│   ├── index.html
│   └── package.json
├── database/init.sql                  # Schema + seed data (auto-applied by MySQL)
├── deploy/                            # Reserved for future Helm chart
└── docker-compose.yaml                # db + backend services
```

---

## 3. Prerequisites

- Docker + Docker Compose (for MySQL and the backend container)
- Python 3.12 + `venv` (for local backend dev / tests)
- Node.js 18+ (for frontend dev)

---

## 4. Quickstart (Docker)

```bash
# Start MySQL + backend (hot-reload)
docker compose up --build

# Backend:  http://localhost:8000        (docs: /docs)
# MySQL:    localhost:3306
```

> `database/init.sql` is mounted at `/docker-entrypoint-initdb.d/init.sql`,
> so the schema and seed data load automatically on first start. If the
> volume already exists with an old schema, reset it with
> `docker compose down -v && docker compose up --build`.

Frontend (runs locally for now — no compose service yet):

```bash
cd frontend/staffsync-frontend
npm install
npm run dev     # http://localhost:5173
```

---

## 5. Environment variables

No secrets are hardcoded. Everything goes through env vars.

### Backend (`src/config/database.py`)

| Variable      | Default       | Compose value |
| ------------- | ------------- | ------------- |
| `DB_HOST`     | `localhost`   | `db`          |
| `DB_PORT`     | `3306`        | `3306`        |
| `DB_USER`     | `api_user`    | `root`        |
| `DB_PASSWORD` | `api_password`| `root`        |
| `DB_NAME`     | `staffsync`   | `staffsync`   |

### Tests (`tests/conftest.py`)

Tests reuse `DB_HOST/DB_PORT/DB_USER/DB_PASSWORD` plus:

| Variable       | Default          | Description                              |
| -------------- | ---------------- | ---------------------------------------- |
| `TEST_DB_NAME` | `staffsync_test` | Isolated DB auto-created for the suite   |

### Frontend

| Variable      | Default                 | Description              |
| ------------- | ----------------------- | ------------------------ |
| `VITE_API_URL`| `http://localhost:8000` | Base URL of the backend  |

---

## 6. Backend

Modular layout: `models/` (SQLAlchemy) ≠ `schemas/` (Pydantic) ≠
`routes/` (endpoints) ≠ `config/` (DB wiring). No security middleware
by design at this stage.

### Run locally (without Docker)

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
DB_HOST=127.0.0.1 DB_USER=root DB_PASSWORD=root \
  uvicorn src.main:app --reload --port 8000
```

### API endpoints

| Method | Path                          | Description                  |
| ------ | ----------------------------- | ---------------------------- |
| GET    | `/`                           | Service status               |
| GET    | `/health`                     | Health check                 |
| GET    | `/api/departments/`           | List departments             |
| POST   | `/api/departments/`           | Create department (201)      |
| GET    | `/api/departments/{id}`       | Get department (404 if none) |
| PUT    | `/api/departments/{id}`       | Update department            |
| DELETE | `/api/departments/{id}`       | Delete department (204)      |
| GET    | `/api/employees/`             | List employees               |
| POST   | `/api/employees/`             | Create employee (201)        |
| GET    | `/api/employees/{id}`         | Get employee (404 if none)   |
| PUT    | `/api/employees/{id}`         | Update employee              |
| DELETE | `/api/employees/{id}`         | Delete employee (204)        |

Validation (Pydantic): `name` 1–100 chars, `email` valid format and
unique (duplicate → 400), `department_id` must exist (unknown → 400).

Interactive docs: `http://localhost:8000/docs`.

### Tests

Tests run **against real MySQL** (no SQLite anywhere in the repo).
`conftest.py` waits for MySQL, creates `TEST_DB_NAME`, runs
`Base.metadata.create_all`, and wipes all tables after each test — the
development `staffsync` database is never touched.

```bash
# MySQL must be up: docker compose up -d db
DB_HOST=127.0.0.1 DB_USER=root DB_PASSWORD=root \
  PYTHONPATH=backend backend/venv/bin/python -m pytest backend/tests/ -v
```

23 tests: health (2), departments CRUD + 404/422 (9), employees CRUD +
duplicate-email 400 / invalid-email 422 / unknown-department 400 (12).

---

## 7. Frontend

- `App.jsx` boots the app: `Navbar` + `Routes` (`/` Home landing,
  `/departments`, `/employees`, 404) + footer.
- `components/Navbar.jsx`: black top bar with brand and menu
  (Home / Departments / Employees); hamburger button with animated X
  on screens ≤ 600px, auto-closes on navigation.
- `pages/Home.jsx`: welcome hero with CTAs plus link cards to both sections.
- `pages/Departments.jsx`: department cards from `GET /api/departments/`.
- `pages/Employees.jsx`: roster stats-table from `GET /api/employees/`
  (+ department names from `GET /api/departments/`).
- `style/global.css`: single global stylesheet, NBA.com-inspired dark
  theme (near-black surfaces, red `#c8102e` / blue `#1d428a` accents,
  condensed uppercase headlines), fully responsive.

```bash
cd frontend/staffsync-frontend
npm install
npm run dev      # local dev with hot-reload
npm run build    # production build
npm run lint     # eslint
```

---

## 8. Database

`database/init.sql`:

- `departments(id, name)`
- `employees(id, name, email UNIQUE, department_id → departments.id
  ON DELETE SET NULL, hire_date DEFAULT CURRENT_TIMESTAMP)`
- Seeds: Engineering, Human Resources, Sales + 2 employees.

---

## 9. CI/CD

`.github/workflows/ci-backend.yaml` triggers on pushes/PRs touching
`backend/**`: spins up a MySQL 8 service container (health-checked),
installs `backend/requirements.txt` on Python 3.11, and runs
`pytest backend/tests/ -v` with `DB_HOST=127.0.0.1`, root credentials.

---

## 10. Roadmap

- [ ] Frontend Docker image + compose service
- [ ] Helm chart under `deploy/`
- [ ] Auth/security middleware, pagination, filtering
- [ ] Frontend CRUD forms (create/update/delete from the UI)
