from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import Response
import json
import wave
from app.core.naver_stt import NaverSTT
import os
import tempfile
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

router = APIRouter()

def get_stt_instance():
    """STT 인스턴스를 생성합니다."""
    access_key = os.getenv("NAVER_CLOUD_ACCESS_KEY")
    secret_key = os.getenv("NAVER_CLOUD_SECRET_KEY")
    
    if not access_key or not secret_key:
        raise ValueError("네이버 클라우드 인증 정보가 설정되지 않았습니다.")
    
    return NaverSTT(access_key, secret_key)

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
                    return Response(
                        status_code=204,
                        content=None,
                        headers={
                            "Content-Length": "0",
                            "Content-Type": "application/json"
                        }
                    )
                
                # JSON 문자열로 변환
                json_str = json.dumps(result)
                
                return Response(
                    content=json_str,
                    media_type="application/json",
                    headers={
                        "Content-Length": str(len(json_str)),
                        "Content-Type": "application/json"
                    }
                )
                
        finally:
            # 임시 파일 삭제
            os.unlink(temp_path)
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recognition failed: {str(e)}") 



@router.post("/file/android/3gp")
async def recognize_file(file: UploadFile = File(...)):
    """음성 파일을 업로드하여 텍스트로 변환합니다."""
    if not file.filename.lower().endswith('.3gp'):  # .wav에서 .3gp로 변경
        raise HTTPException(status_code=400, detail="Only 3GP files are supported")
    
    try:
        # 임시 파일로 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix='.3gp') as temp_file:  # .wav에서 .3gp로 변경
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
        try:
            # 3GP 파일을 WAV로 변환
            wav_path = temp_path.replace('.3gp', '.wav')
            convert_3gp_to_wav(temp_path, wav_path)
            
            # WAV 파일 검증 및 파라미터 추출
            audio_params = validate_wav_file(wav_path)
            
            # 음성 인식 수행
            with wave.open(wav_path, "rb") as wf:
                audio_data = wf.readframes(wf.getnframes())
                stt = get_stt_instance()
                result = stt.recognize(
                    audio_data,
                    sample_rate=audio_params["sample_rate"],
                    channels=audio_params["channels"],
                    sample_width=audio_params["sample_width"]
                )
                
                if not result["text"]:
                    return Response(
                        status_code=204,
                        content=None,
                        headers={
                            "Content-Length": "0",
                            "Content-Type": "application/json"
                        }
                    )
                
                # JSON 문자열로 변환
                json_str = json.dumps(result)
                
                return Response(
                    content=json_str,
                    media_type="application/json",
                    headers={
                        "Content-Length": str(len(json_str)),
                        "Content-Type": "application/json"
                    }
                )
                
        finally:
            # 임시 파일 삭제
            os.unlink(temp_path)
            if os.path.exists(wav_path):
                os.unlink(wav_path)
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recognition failed: {str(e)}")

def convert_3gp_to_wav(input_path: str, output_path: str):
    """3GP 파일을 WAV로 변환합니다."""
    try:
        # ffmpeg를 사용하여 변환
        import subprocess
        subprocess.run([
            'ffmpeg',
            '-i', input_path,
            '-acodec', 'pcm_s16le',
            '-ar', '16000',
            '-ac', '1',
            output_path
        ], check=True)
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Failed to convert 3GP to WAV: {str(e)}")