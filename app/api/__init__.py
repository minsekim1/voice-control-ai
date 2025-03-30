from fastapi import APIRouter
from app.api.endpoints import recognition

router = APIRouter()

router.include_router(recognition.router, prefix="/recognition", tags=["recognition"])