from fastapi import APIRouter, WebSocket, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import json
import wave
import numpy as np
from app.core.stt import VoskSTT
from app.schemas.recognition import RecognitionResponse
import os
import tempfile

router = APIRouter()

def get_stt_instance():
    """STT 인스턴스를 생성합니다."""
    return VoskSTT()

def validate_wav_file(file_path):
    """WAV 파일의 형식을 검증합니다."""
    try:
        with wave.open(file_path, "rb") as wf:
            if wf.getnchannels() != 1:
                raise ValueError("Audio must be mono")
            if wf.getsampwidth() != 2:
                raise ValueError("Audio must be 16-bit")
            if wf.getframerate() not in [16000, 44100, 48000]:
                raise ValueError("Sample rate must be 16000, 44100, or 48000 Hz")
            return {
                "sample_rate": wf.getframerate(),
                "channels": wf.getnchannels(),
                "sample_width": wf.getsampwidth()
            }
    except wave.Error:
        raise ValueError("Invalid WAV file")

@router.post("/file")
async def recognize_file(file: UploadFile = File(...)):
    """음성 파일을 업로드하여 텍스트로 변환합니다."""
    if not file.filename.lower().endswith('.wav'):
        raise HTTPException(status_code=400, detail="Only WAV files are supported")
    
    try:
        # 임시 파일로 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
        try:
            # WAV 파일 검증 및 파라미터 추출
            audio_params = validate_wav_file(temp_path)
            
            # 음성 인식 수행
            with wave.open(temp_path, "rb") as wf:
                audio_data = wf.readframes(wf.getnframes())
                stt = get_stt_instance()
                result = stt.recognize(
                    audio_data,
                    sample_rate=audio_params["sample_rate"],
                    channels=audio_params["channels"],
                    sample_width=audio_params["sample_width"]
                )
                
                if not result["text"]:
                    return JSONResponse(
                        status_code=204,
                        content=None,
                        headers={"Content-Length": "0"}
                    )
                
                return JSONResponse(
                    content=result,
                    headers={"Content-Type": "application/json"}
                )
                
        finally:
            # 임시 파일 삭제
            os.unlink(temp_path)
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recognition failed: {str(e)}")

@router.websocket("/stream")
async def stream_recognition(websocket: WebSocket):
    """WebSocket을 통한 실시간 음성 스트리밍 인식"""
    await websocket.accept()
    stt = get_stt_instance()
    
    try:
        while True:
            # 클라이언트로부터 오디오 데이터 수신
            audio_data = await websocket.receive_bytes()
            
            try:
                # Vosk로 음성 인식
                result = stt.recognize(audio_data)
                
                # 결과 전송
                if result["text"]:
                    await websocket.send_json(result)
                    
            except Exception as e:
                await websocket.send_json({
                    "error": str(e),
                    "text": "",
                    "confidence": 0.0
                })
                
    except Exception as e:
        await websocket.close(code=1000, reason=str(e)) 