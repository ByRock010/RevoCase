from pydantic import BaseModel
from datetime import datetime


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CompanyCreate(BaseModel):
    name: str
    hq: str
    website: str


class CompetitorResponse(BaseModel):
    id: int
    name: str
    summary: str | None

    class Config:
        from_attributes = True


class CompanyResponse(BaseModel):
    id: int
    name: str
    hq: str
    website: str
    summary: str | None
    created_at: datetime
    competitors: list[CompetitorResponse]

    class Config:
        from_attributes = True
