# CLAUDE.md — RevoCase Project Context

> **Important:** Always update this file after making changes to the project so future conversations have full context.

## Project Overview

RevoCase is a company intelligence platform where an admin user can log in, submit a company, and view AI-generated summaries along with 5 competitors. Built as a case study for Revo.

## Tech Stack

- **Frontend:** React 18 + Vite (in `ui/`)
- **Backend:** Python 3.12 + FastAPI (in `api/`)
- **Database:** PostgreSQL on Supabase (cloud, Mumbai/ap-south-1 region)
- **AI:** OpenAI GPT-4o-mini for company analysis
- **Deployment target:** Frontend on Cloudflare Pages (`revocase.bahabayrakcioglu.com`), Backend on Railway

## Key Credentials & Config

- **Admin login:** username `admin`, password `Revo123456.`
- **Supabase project ref:** `rqryhnnzpvdzdybzeamj`
- **Supabase region:** ap-south-1 (Mumbai)
- **Database connection uses Session Pooler** (IPv4 compatible): `aws-1-ap-south-1.pooler.supabase.com:5432`
- **Direct connection (`db.*.supabase.co`) does NOT work** — IPv6 only, user's network is IPv4
- **Database password contains `%` characters** — must be URL-encoded as `%25` in connection strings
- Environment variables are in `api/.env` (git-ignored), examples in `api/.env.example` and `ui/.env.example`

## Project Structure

```
RevoCase/
├── api/                        # FastAPI backend
│   ├── app/
│   │   ├── main.py             # Routes: /health, /auth/login, /companies CRUD
│   │   ├── models.py           # SQLAlchemy: Company, Competitor (one-to-many)
│   │   ├── schemas.py          # Pydantic: LoginRequest, CompanyCreate, CompanyResponse
│   │   ├── auth.py             # JWT auth (python-jose, HS256, 60min expiry)
│   │   ├── ai_service.py       # OpenAI GPT-4o-mini integration
│   │   ├── config.py           # Loads env vars from .env
│   │   └── database.py         # SQLAlchemy engine + session
│   ├── Dockerfile, Procfile     # Railway deployment
│   └── requirements.txt
├── ui/                         # React SPA
│   ├── src/
│   │   ├── pages/LoginPage.jsx, HomePage.jsx
│   │   ├── components/CreateModal.jsx, CompanyCard.jsx
│   │   ├── api.js              # Axios client with JWT interceptor
│   │   └── App.jsx             # React Router with ProtectedRoute
│   ├── public/_redirects       # Cloudflare Pages SPA fallback
│   ├── Dockerfile, nginx.conf  # Docker deployment
│   └── vite.config.js
├── docker-compose.yml          # Local dev (loads api/.env, has local Postgres as fallback)
├── README.md
├── ARCHITECTURE.md
└── CLAUDE.md                   # This file
```

## Database Schema (Supabase)

- **companies**: id, name, hq, website, summary (text), created_at
- **competitors**: id, company_id (FK → companies.id CASCADE), name, summary (text)
- Tables are auto-created via `Base.metadata.create_all()` on backend startup

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | /health | No | Health check |
| POST | /auth/login | No | Returns JWT |
| POST | /companies | Yes | Create company + AI analysis |
| GET | /companies | Yes | List all companies |
| GET | /companies/{id} | Yes | Get single company |
| DELETE | /companies/{id} | Yes | Delete company |

Swagger docs available at `/docs`.

## Docker Setup

- `docker-compose.yml` uses `env_file: ./api/.env` to load all backend env vars
- The `DATABASE_URL` in `.env` points to Supabase (not the local Docker Postgres)
- The `FRONTEND_URL` is overridden in docker-compose to `http://localhost:5173` for local dev
- UI container uses nginx for serving the built React app

## Known Gotchas

1. **Supabase password encoding:** Password has `%` chars — use `%25` in URL-encoded connection strings
2. **Supabase IPv4:** Must use Session Pooler (`aws-1-ap-south-1.pooler.supabase.com`), NOT direct connection
3. **CORS:** Backend allows `FRONTEND_URL`, `localhost:5173`, and `localhost:3000`
4. **AI call can be slow:** OpenAI call takes a few seconds; frontend shows spinner during creation

## Enhancements Added (beyond requirements)

- **Structured JSON output:** `response_format={"type": "json_object"}` on OpenAI call — eliminates JSON parsing failures
- **Enhanced AI prompt:** Role-based prompt with specific instructions for each bullet point (what they do, market position, key differentiator, etc.)
- **Swagger tags:** Endpoints grouped under "System", "Authentication", "Companies" for cleaner API docs
- **Docstrings on endpoints:** Appear in Swagger UI as descriptions
- **Backend logging:** Logs company creation/deletion and AI errors for observability
- **Improved .env.example files:** Both show local and production values with clear comments
- **Env var validation:** `config.py` raises clear errors if `DATABASE_URL` or `OPENAI_API_KEY` are missing
- **Error state on HomePage:** Shows error message + retry button if company list fails to load
- **Auto-expand new company:** Newly created company card auto-expands and scrolls into view
- **Revo Capital design:** UI styled to match revo.vc — navy #293E56, gold #E4C06E, off-white #F8F7EE, Montserrat font, pill buttons

## Deployment Status

- [ ] Backend deployed to Railway
- [ ] Frontend deployed to Cloudflare Pages at `revocase.bahabayrakcioglu.com`
- [x] Database tables created in Supabase
- [x] Docker local setup working
