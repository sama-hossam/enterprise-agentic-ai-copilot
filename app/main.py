
from fastapi import FastAPI
from app.api.routes.health import router as system_router
from app.core.config import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name, version=settings.app_version)
app.include_router(system_router)
