from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class ServerSettings(BaseModel):
    language: str = "ko"
    model_path: str = "model/vosk-model-small-ko-0.22"
    sample_rate: int = 16000
    channels: int = 1

@router.get("/", response_model=ServerSettings)
async def get_settings():
    """
    현재 서버 설정을 반환합니다.
    """
    return ServerSettings()

@router.put("/", response_model=ServerSettings)
async def update_settings(settings: ServerSettings):
    """
    서버 설정을 업데이트합니다.
    """
    try:
        # TODO: 설정 저장 및 적용 로직 구현
        return settings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 