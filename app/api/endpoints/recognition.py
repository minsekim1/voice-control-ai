from fastapi import APIRouter, WebSocket, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import json
import wave
import numpy as np
from app.core.stt import VoskSTT
from app.schemas.recognition import RecognitionResponse

router = APIRouter()
stt = VoskSTT()

@router.post("/file", response_model=RecognitionResponse)
async def recognize_file(file: UploadFile = File(...)):
    """
    음성 파일을 업로드하여 텍스트로 변환합니다.
    """
    try:
        # 임시 파일로 저장
        with open("temp.wav", "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # WAV 파일 처리
        with wave.open("temp.wav", "rb") as wf:
            # 오디오 데이터 읽기
            audio_data = wf.readframes(wf.getnframes())
            
            # Vosk로 음성 인식
            result = stt.recognize(audio_data)
            
            return RecognitionResponse(
                text=result["text"],
                confidence=result.get("confidence", 0.0)
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.websocket("/stream")
async def stream_recognition(websocket: WebSocket):
    """
    WebSocket을 통한 실시간 음성 스트리밍 인식
    """
    await websocket.accept()
    
    try:
        while True:
            # 클라이언트로부터 오디오 데이터 수신
            audio_data = await websocket.receive_bytes()
            
            # Vosk로 음성 인식
            result = stt.recognize(audio_data)
            
            # 결과 전송
            await websocket.send_json(result)
            
    except Exception as e:
        await websocket.close(code=1000, reason=str(e)) 