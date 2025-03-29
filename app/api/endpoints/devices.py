from fastapi import APIRouter, HTTPException
import sounddevice as sd

router = APIRouter()

@router.get("/list")
async def list_devices():
    """
    사용 가능한 오디오 장치 목록을 반환합니다.
    """
    try:
        devices = sd.query_devices()
        return {
            "devices": [
                {
                    "id": i,
                    "name": device["name"],
                    "max_input_channels": device["max_input_channels"],
                    "max_output_channels": device["max_output_channels"],
                    "default_samplerate": device["default_samplerate"]
                }
                for i, device in enumerate(devices)
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/default")
async def get_default_device():
    """
    기본 입력 장치 정보를 반환합니다.
    """
    try:
        default_device = sd.query_devices(kind="input")
        return {
            "id": default_device["index"],
            "name": default_device["name"],
            "max_input_channels": default_device["max_input_channels"],
            "default_samplerate": default_device["default_samplerate"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 