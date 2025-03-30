from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import Response
import json
import wave
from app.core.naver_stt import NaverSTT
import os
import tempfile
from dotenv import load_dotenv
import logging

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 환경 변수 로드
load_dotenv()

router = APIRouter()

def get_stt_instance():
    """STT 인스턴스를 생성합니다."""
    access_key = os.getenv("NAVER_CLOUD_ACCESS_KEY")
    secret_key = os.getenv("NAVER_CLOUD_SECRET_KEY")
    
    if not access_key or not secret_key:
        logger.error("네이버 클라우드 인증 정보가 설정되지 않았습니다.")
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
    except wave.Error as e:
        logger.error(f"WAV 파일 검증 중 오류 발생: {str(e)}")
        raise ValueError("Invalid WAV file")

@router.post("/file")
async def recognize_file(file: UploadFile = File(...)):
    """음성 파일을 업로드하여 텍스트로 변환합니다."""
    logger.info(f"파일 업로드 시작: {file.filename}")
    
    if not file.filename.lower().endswith('.wav'):
        logger.error(f"지원하지 않는 파일 형식: {file.filename}")
        raise HTTPException(status_code=400, detail="Only WAV files are supported")
    
    try:
        # 임시 파일로 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
            logger.debug(f"임시 파일 생성: {temp_path}")
        
        try:
            # WAV 파일 검증 및 파라미터 추출
            audio_params = validate_wav_file(temp_path)
            logger.debug(f"오디오 파라미터: {audio_params}")
            
            # 음성 인식 수행
            with wave.open(temp_path, "rb") as wf:
                audio_data = wf.readframes(wf.getnframes())
                stt = get_stt_instance()
                logger.info("음성 인식 시작")
                result = stt.recognize(
                    audio_data,
                    sample_rate=audio_params["sample_rate"],
                    channels=audio_params["channels"],
                    sample_width=audio_params["sample_width"]
                )
                logger.info(f"음성 인식 결과: {result}")
                
                if not result["text"]:
                    logger.warning("인식된 텍스트가 없습니다")
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
                
        except Exception as e:
            logger.error(f"음성 인식 중 오류 발생: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Recognition failed: {str(e)}")
        finally:
            # 임시 파일 삭제
            try:
                os.unlink(temp_path)
                logger.debug("임시 파일 삭제 완료")
            except Exception as e:
                logger.error(f"임시 파일 삭제 중 오류 발생: {str(e)}")
            
    except ValueError as e:
        logger.error(f"파일 검증 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"예상치 못한 오류 발생: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.post("/file/android/3gp")
async def recognize_3gp_file(file: UploadFile = File(...)):
    """3GP 음성 파일을 업로드하여 텍스트로 변환합니다."""
    logger.info(f"3GP 파일 업로드 시작: {file.filename}")
    
    if not file.filename.lower().endswith('.3gp'):
        logger.error(f"지원하지 않는 파일 형식: {file.filename}")
        raise HTTPException(status_code=400, detail="Only 3GP files are supported")
    
    try:
        # 임시 파일로 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix='.3gp') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
            logger.debug(f"임시 파일 생성: {temp_path}")
        
        try:
            # 음성 인식 수행
            with open(temp_path, "rb") as f:
                audio_data = f.read()
                stt = get_stt_instance()
                logger.info("음성 인식 시작")
                result = stt.recognize(
                    audio_data,
                    format="3gp"
                )
                logger.info(f"음성 인식 결과: {result}")
                
                if not result["text"]:
                    logger.warning("인식된 텍스트가 없습니다")
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
                
        except Exception as e:
            logger.error(f"음성 인식 중 오류 발생: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Recognition failed: {str(e)}")
        finally:
            # 임시 파일 삭제
            try:
                os.unlink(temp_path)
                logger.debug("임시 파일 삭제 완료")
            except Exception as e:
                logger.error(f"임시 파일 삭제 중 오류 발생: {str(e)}")
            
    except ValueError as e:
        logger.error(f"파일 검증 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"예상치 못한 오류 발생: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

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