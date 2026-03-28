# Architecture

## Overview

RevoCase follows a standard three-tier architecture: a React single-page application (SPA) communicates with a FastAPI backend, which persists data in a PostgreSQL database hosted on Supabase.

```
┌─────────────────┐     HTTPS      ┌─────────────────┐     TCP       ┌─────────────────┐
│                 │  ──────────▶   │                 │  ──────────▶  │                 │
│   React SPA     │                │   FastAPI       │               │   PostgreSQL    │
│   (Cloudflare)  │  ◀──────────  │   (Railway)     │  ◀──────────  │   (Supabase)    │
│                 │     JSON       │                 │     SQL       │                 │
└─────────────────┘                └────────┬────────┘               └─────────────────┘
                                            │
                                            │ HTTPS
                                            ▼
                                   ┌─────────────────┐
                                   │  OpenAI GPT   │
                                   │  AI API          │
                                   └─────────────────┘
```

## Frontend (ui/)

- **Framework**: React 18 with Vite
- **Routing**: React Router v6 with client-side routing
- **HTTP Client**: Axios with request/response interceptors for JWT
- **Hosting**: Cloudflare Pages with `_redirects` for SPA fallback

### Key Components

| Component      | Purpose                                              |
|---------------|------------------------------------------------------|
| `App.jsx`      | Route definitions and auth guard (`ProtectedRoute`)  |
| `LoginPage`    | Login form, calls `/auth/login`, stores JWT          |
| `HomePage`     | Lists companies, hosts Create button and modal       |
| `CreateModal`  | Form to submit company details, triggers AI analysis |
| `CompanyCard`  | Expandable card showing summary and competitors      |
| `api.js`       | Axios instance with auth interceptors                |

## Backend (api/)

- **Framework**: FastAPI (Python 3.12)
- **ORM**: SQLAlchemy 2.0 with declarative models
- **Auth**: JWT tokens via `python-jose`, stateless authentication
- **Hosting**: Railway with Procfile-based deployment

### API Endpoints

| Method   | Path                    | Auth | Description                  |
|----------|------------------------|------|------------------------------|
| `GET`    | `/health`              | No   | Health check                 |
| `POST`   | `/auth/login`          | No   | Authenticate and get JWT     |
| `POST`   | `/companies`           | Yes  | Create company + AI analysis |
| `GET`    | `/companies`           | Yes  | List all companies           |
| `GET`    | `/companies/{id}`      | Yes  | Get single company           |
| `DELETE` | `/companies/{id}`      | Yes  | Delete a company             |

### Request Flow (Company Creation)

1. Frontend sends `POST /companies` with `{name, hq, website}` + JWT
2. Backend validates the token
3. Backend calls OpenAI GPT API with a structured prompt
4. OpenAI returns JSON with company summary + 5 competitors
5. Backend persists the company and competitors to PostgreSQL
6. Full company object (with competitors) returned to frontend

## Database

### Schema

```
companies
├── id          (PK, serial)
├── name        (varchar 255)
├── hq          (varchar 255)
├── website     (varchar 500)
├── summary     (text)
└── created_at  (timestamptz)

competitors
├── id          (PK, serial)
├── company_id  (FK → companies.id, CASCADE)
├── name        (varchar 255)
└── summary     (text)
```

A company has many competitors (one-to-many). Deleting a company cascades to its competitors.

## Authentication Flow

1. User submits username/password to `/auth/login`
2. Backend validates against hardcoded admin credentials
3. On success, returns a signed JWT (HS256, 60-minute expiry)
4. Frontend stores the token in `localStorage`
5. All subsequent API requests include `Authorization: Bearer <token>`
6. On 401 response, the Axios interceptor clears the token and redirects to login

## AI Integration

- **Model**: OpenAI GPT-4o-mini
- **Approach**: Structured prompt requesting JSON output with company summary and 5 competitors
- **Each summary**: 4-5 concise bullet points
- **Error handling**: Returns 502 if the AI service fails

## Deployment

| Service    | Platform         | Config              |
|-----------|-----------------|---------------------|
| Frontend  | Cloudflare Pages | Build: `npm run build`, Output: `dist` |
| Backend   | Railway          | Procfile, env vars  |
| Database  | Supabase         | Managed PostgreSQL  |
