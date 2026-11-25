from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1", tags=["health"])


class AccessSimulationRequest(BaseModel):
    user_id: str = Field(min_length=1)
    access_point: str = Field(min_length=1)
    occurred_at: datetime | None = None


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/access-attempts/simulate", status_code=201)
def simulate_access(request: AccessSimulationRequest) -> dict[str, str]:
    """Placeholder da borda HTTP; o caso de uso será injetado no próximo ciclo."""
    return {
        "user_id": request.user_id,
        "access_point": request.access_point,
        "status": "use_case_not_wired",
    }
