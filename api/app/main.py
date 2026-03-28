import logging
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import engine, get_db, Base
from app.models import Company, Competitor
from app.schemas import LoginRequest, TokenResponse, CompanyCreate, CompanyResponse
from app.auth import authenticate_user, create_access_token, get_current_user
from app.ai_service import generate_company_analysis
from app.config import FRONTEND_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RevoCase API",
    description="Company analysis tool with AI-generated summaries and competitor insights",
    version="1.0.0",
)

origins = [
    FRONTEND_URL,
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}


@app.post("/auth/login", response_model=TokenResponse, tags=["Authentication"])
def login(request: LoginRequest):
    """Authenticate with admin credentials and receive a JWT token."""
    if not authenticate_user(request.username, request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    token = create_access_token(request.username)
    logger.info("Admin user logged in")
    return TokenResponse(access_token=token)


@app.post("/companies", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED, tags=["Companies"])
def create_company(
    data: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    """Create a new company and generate AI-powered analysis with 5 competitors."""
    logger.info(f"Creating company: {data.name}")

    # Generate AI analysis
    try:
        analysis = generate_company_analysis(data.name, data.hq, data.website)
    except Exception as e:
        logger.error(f"AI service error for {data.name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI service error: {str(e)}",
        )

    # Create company
    company = Company(
        name=data.name,
        hq=data.hq,
        website=data.website,
        summary=analysis.get("company_summary", ""),
    )
    db.add(company)
    db.flush()

    # Create competitors
    for comp in analysis.get("competitors", []):
        competitor = Competitor(
            company_id=company.id,
            name=comp.get("name", "Unknown"),
            summary=comp.get("summary", ""),
        )
        db.add(competitor)

    db.commit()
    db.refresh(company)
    logger.info(f"Company created: {company.name} (id={company.id}) with {len(company.competitors)} competitors")
    return company


@app.get("/companies", response_model=list[CompanyResponse], tags=["Companies"])
def list_companies(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    """List all companies with their AI-generated summaries and competitors."""
    companies = db.query(Company).order_by(Company.created_at.desc()).all()
    return companies


@app.get("/companies/{company_id}", response_model=CompanyResponse, tags=["Companies"])
def get_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    """Get a specific company by ID with its competitors."""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return company


@app.delete("/companies/{company_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Companies"])
def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    """Delete a company and all its associated competitors."""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    db.delete(company)
    db.commit()
    logger.info(f"Company deleted: {company.name} (id={company.id})")
