from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.config import get_settings
from app.infrastructure.database import get_db
from app.infrastructure.repositories import SqlAlchemyUserRepository
from app.infrastructure.security import create_access_token, verify_password

settings = get_settings()
router = APIRouter(prefix=f"{settings.api_v1_prefix}/auth", tags=["authentication"])


class LoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=8, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, session: Session = Depends(get_db)) -> TokenResponse:
    return _login(request, session)


def _login(request: LoginRequest, session: Session) -> TokenResponse:
    user = SqlAlchemyUserRepository(session).get_by_email(request.email.strip())
    if user is None or not user.active or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenResponse(access_token=create_access_token(user.id, user.role, settings))
