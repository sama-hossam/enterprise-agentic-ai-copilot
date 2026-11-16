from fastapi import APIRouter
from app.core.config import get_settings

router = APIRouter(tags=["system"])

@router.get("/health")
def health():
    settings = get_settings()
    return {"status": "healthy", "service": settings.app_name, "version": settings.app_version}
