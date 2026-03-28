# RevoCase - Company Intelligence Platform

A lightweight web application where an admin user can log in, submit a company, and view AI-generated summaries along with 5 competitors.

## Live Deployment

- **Frontend**: [revocase.bahabayrakcioglu.com](https://revocase.bahabayrakcioglu.com) (Cloudflare Pages)
- **Backend API**: Deployed on Railway
- **API Docs (Swagger)**: `<railway-url>/docs`
- **Database**: Supabase (PostgreSQL)

## Tech Stack

| Layer      | Technology              |
|------------|------------------------|
| Frontend   | React + Vite           |
| Backend    | Python + FastAPI       |
| Database   | PostgreSQL (Supabase)  |
| AI         | OpenAI GPT-4o          |
| Hosting    | Cloudflare Pages + Railway |

## Project Structure

```
RevoCase/
├── api/                    # FastAPI backend
│   ├── app/
│   │   ├── main.py         # FastAPI application & routes
│   │   ├── models.py       # SQLAlchemy database models
│   │   ├── schemas.py      # Pydantic request/response schemas
│   │   ├── auth.py         # JWT authentication logic
│   │   ├── ai_service.py   # OpenAI GPT integration
│   │   ├── config.py       # Environment configuration
│   │   └── database.py     # Database connection setup
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── Procfile            # Railway deployment
│   └── .env.example
├── ui/                     # React frontend
│   ├── src/
│   │   ├── pages/          # LoginPage, HomePage
│   │   ├── components/     # CreateModal, CompanyCard
│   │   ├── api.js          # Axios API client
│   │   ├── App.jsx         # Router setup
│   │   └── main.jsx        # Entry point
│   ├── Dockerfile
│   └── .env.example
├── docker-compose.yml      # Local development with Docker
├── README.md
└── ARCHITECTURE.md
```

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.12+
- An OpenAI API key

### Environment Variables

Copy the example env files and fill in values:

```bash
cp api/.env.example api/.env
cp ui/.env.example ui/.env
```

**api/.env** requires:
- `DATABASE_URL` - PostgreSQL connection string
- `OPENAI_API_KEY` - OpenAI API key
- `JWT_SECRET_KEY` - Secret for JWT token signing

**ui/.env** requires:
- `VITE_API_URL` - Backend API URL

### Run Locally

**Backend:**
```bash
cd api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd ui
npm install
npm run dev
```

### Run with Docker

```bash
docker-compose up --build
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs

## Login Credentials

- **Username:** admin
- **Password:** Revo123456.

## Features

1. **Authentication** - JWT-based login with admin credentials
2. **Company Creation** - Submit company name, HQ, and website
3. **AI Analysis** - OpenAI GPT-4o generates a summary + 5 competitors with bullet points
4. **Persistent History** - All companies stored in PostgreSQL and displayed on homepage
5. **Swagger Docs** - Full API documentation at `/docs`
