from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.api.auth import router as auth_router
from app.api.routes import router
from app.api.users import router as users_router
from app.config import get_settings
from app.infrastructure.database import init_db

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0")
app.include_router(router)
app.include_router(auth_router)
app.include_router(users_router)


@app.get("/", include_in_schema=False)
def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse(url="/docs", status_code=307)


@app.on_event("startup")
def create_tables() -> None:
    init_db()
