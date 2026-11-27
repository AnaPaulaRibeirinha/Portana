from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.api.dependencies import get_access_service, require_roles
from app.application.access_service import AccessService
from app.config import get_settings
from app.domain.access import UserRole

router = APIRouter(prefix=get_settings().api_v1_prefix, tags=["health"])


class AccessSimulationRequest(BaseModel):
    user_id: str = Field(min_length=1)
    access_point: str = Field(min_length=1)
    occurred_at: datetime | None = None


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/access-attempts/simulate", status_code=201)
def simulate_access(
    request: AccessSimulationRequest,
    service: AccessService = Depends(get_access_service),
    _current_user=Depends(require_roles(UserRole.ADMIN, UserRole.PORTEIRO)),
) -> dict[str, str]:
    attempt = service.simulate(
        user_id=request.user_id,
        access_point=request.access_point,
        at=request.occurred_at or datetime.now(),
    )
    return {
        "user_id": attempt.user_id,
        "access_point": attempt.access_point,
        "decision": attempt.decision.value,
        "occurred_at": attempt.occurred_at.isoformat(),
    }
