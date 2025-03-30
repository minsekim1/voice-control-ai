from fastapi import APIRouter, HTTPException
import sounddevice as sd

router = APIRouter()

@router.get("/list")
async def list_devices():
    """사용 가능한 오디오 장치 목록을 반환합니다."""
    try:
        devices = sd.query_devices()
        return {"devices": [{"name": d["name"], "index": i} for i, d in enumerate(devices)]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/default")
async def get_default_devices():
    """기본 입력/출력 장치 정보를 반환합니다."""
    try:
        input_device = sd.query_devices(kind="input")
        output_device = sd.query_devices(kind="output")
        return {
            "input": {
                "name": input_device["name"],
                "index": sd.default.device[0]
            },
            "output": {
                "name": output_device["name"],
                "index": sd.default.device[1]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 