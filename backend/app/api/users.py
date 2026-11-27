from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, require_roles
from app.config import get_settings
from app.domain.access import UserRole
from app.infrastructure.database import get_db
from app.infrastructure.models import UserModel
from app.infrastructure.repositories import SqlAlchemyUserRepository
from app.infrastructure.security import hash_password

router = APIRouter(prefix=f"{get_settings().api_v1_prefix}/users", tags=["users"])


class UserCreateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=8, max_length=128)
    role: UserRole = UserRole.MORADOR


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: UserRole
    active: bool


@router.get("/me", response_model=UserResponse)
def get_profile(current_user: UserModel = Depends(get_current_user)) -> UserModel:
    return current_user


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(UserRole.ADMIN))],
)
def create_user(request: UserCreateRequest, session: Session = Depends(get_db)) -> UserModel:
    email = request.email.strip().lower()
    if SqlAlchemyUserRepository(session).get_by_email(email) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="E-mail já cadastrado")

    user = UserModel(
        id=str(uuid4()),
        name=request.name.strip(),
        email=email,
        password_hash=hash_password(request.password),
        role=request.role.value,
        active=True,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
