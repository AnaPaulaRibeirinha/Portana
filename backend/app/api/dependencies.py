from collections.abc import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.application.access_service import AccessService
from app.config import get_settings
from app.domain.access import UserRole
from app.infrastructure.adapters import LoggingAccessEventPublisher, LoggingNotificationSender
from app.infrastructure.database import get_db
from app.infrastructure.repositories import (
    SqlAlchemyAccessAttemptRepository,
    SqlAlchemySubjectRepository,
    SqlAlchemyUserRepository,
)
from app.infrastructure.security import decode_access_token
from app.infrastructure.models import UserModel

bearer_scheme = HTTPBearer()


def get_access_service(session: Session = Depends(get_db)) -> Generator[AccessService, None, None]:
    yield AccessService(
        subjects=SqlAlchemySubjectRepository(session),
        attempts=SqlAlchemyAccessAttemptRepository(session),
        events=LoggingAccessEventPublisher(),
        notifications=LoggingNotificationSender(),
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: Session = Depends(get_db),
) -> UserModel:
    try:
        payload = decode_access_token(credentials.credentials, get_settings())
        user_id = payload.get("sub")
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido") from error
    if not isinstance(user_id, str):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    user = SqlAlchemyUserRepository(session).get_by_id(user_id)
    if user is None or not user.active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário inválido")
    return user


def require_roles(*allowed_roles: UserRole):
    def dependency(current_user: UserModel = Depends(get_current_user)) -> UserModel:
        if current_user.role not in {role.value for role in allowed_roles}:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Perfil sem permissão")
        return current_user

    return dependency
