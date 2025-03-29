from fastapi import APIRouter
from app.api.endpoints import recognition, devices, settings

router = APIRouter()

router.include_router(recognition.router, prefix="/recognition", tags=["recognition"])
router.include_router(devices.router, prefix="/devices", tags=["devices"])
router.include_router(settings.router, prefix="/settings", tags=["settings"]) 