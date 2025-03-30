import requests
import json
import os
import wave
import io
import tempfile
import ffmpeg
from typing import Dict, Any, Optional

class NaverSTTError(Exception):
    """네이버 클라우드 STT API 관련 예외 클래스"""
    pass

class NaverSTT:
    """네이버 클라우드 STT(Speech-to-Text) 클래스"""
    
    # API 제한사항
    MAX_FILE_SIZE = 3 * 1024 * 1024  # 3MB
    MAX_AUDIO_LENGTH = 60  # 60초
    MIN_AUDIO_LENGTH = 0.4  # 400ms
    
    # 지원하는 언어
    SUPPORTED_LANGUAGES = ["Kor", "Eng"]
    
    def __init__(self, client_id: str, client_secret: str):
        """
        네이버 클라우드 STT 초기화
        
        Args:
            client_id: 네이버 클라우드 Client ID
            client_secret: 네이버 클라우드 Client Secret
        """
        self.api_url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt"
        self.client_id = client_id
        self.client_secret = client_secret
        
    def convert_to_wav(self, audio_data: bytes, format: str = "3gp") -> bytes:
        """
        오디오 파일을 WAV 형식으로 변환
        
        Args:
            audio_data: 원본 오디오 데이터
            format: 원본 오디오 형식 (3gp, mp3 등)
            
        Returns:
            bytes: WAV 형식의 오디오 데이터
        """
        try:
            # 임시 파일 생성
            with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{format}') as input_file:
                input_file.write(audio_data)
                input_path = input_file.name
            
            output_path = input_path.replace(f'.{format}', '.wav')
            
            # ffmpeg를 사용하여 WAV로 변환
            stream = ffmpeg.input(input_path)
            stream = ffmpeg.output(
                stream,
                output_path,
                acodec='pcm_s16le',
                ac=1,
                ar=16000
            )
            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
            
            # 변환된 WAV 파일 읽기
            with open(output_path, 'rb') as f:
                wav_data = f.read()
            
            # 임시 파일 삭제
            os.unlink(input_path)
            os.unlink(output_path)
            
            return wav_data
            
        except Exception as e:
            raise NaverSTTError(f"오디오 변환 중 오류 발생: {str(e)}")
        
    def validate_audio_file(self, audio_data: bytes) -> Dict[str, Any]:
        """
        오디오 파일 유효성 검사
        
        Args:
            audio_data: WAV 형식의 바이너리 음성 데이터
            
        Returns:
            Dict[str, Any]: 오디오 파일 정보
            {
                "sample_rate": 샘플링 레이트,
                "channels": 채널 수,
                "sample_width": 샘플 너비,
                "duration": 재생 시간(초)
            }
            
        Raises:
            NaverSTTError: 오디오 파일이 유효하지 않은 경우
        """
        try:
            # 파일 크기 검사
            if len(audio_data) > self.MAX_FILE_SIZE:
                raise NaverSTTError("음성 데이터가 허용 용량을 초과했습니다 (최대 3MB)")
            
            # WAV 파일 검증
            with wave.open(io.BytesIO(audio_data), "rb") as wf:
                sample_rate = wf.getframerate()
                channels = wf.getnchannels()
                sample_width = wf.getsampwidth()
                duration = wf.getnframes() / sample_rate
                
                # 재생 시간 검사
                if duration > self.MAX_AUDIO_LENGTH:
                    raise NaverSTTError("음성 데이터가 허용 길이를 초과했습니다 (최대 60초)")
                if duration < self.MIN_AUDIO_LENGTH:
                    raise NaverSTTError("음성 데이터가 너무 짧습니다 (최소 400ms)")
                
                return {
                    "sample_rate": sample_rate,
                    "channels": channels,
                    "sample_width": sample_width,
                    "duration": duration
                }
                
        except wave.Error:
            raise NaverSTTError("유효하지 않은 WAV 파일입니다")
            
    def recognize(self, audio_data: bytes, sample_rate: int = 16000, 
                 channels: int = 1, sample_width: int = 2, lang: str = "Kor",
                 format: str = "wav") -> Dict[str, Any]:
        """
        음성 데이터를 텍스트로 변환
        
        Args:
            audio_data: 오디오 데이터
            sample_rate: 샘플링 레이트 (기본값: 16000)
            channels: 채널 수 (기본값: 1, 모노)
            sample_width: 샘플 너비 (기본값: 2, 16-bit)
            lang: 인식할 언어 (Kor, Eng, Jpn, Chn)
            format: 오디오 형식 (wav, 3gp 등)
            
        Returns:
            Dict[str, Any]: 인식 결과를 담은 딕셔너리
            {
                "text": "인식된 텍스트",
                "confidence": 신뢰도 점수 (0.0 ~ 1.0)
            }
            
        Raises:
            NaverSTTError: 음성 인식 중 오류가 발생한 경우
        """
        try:
            # 언어 검증
            if lang not in self.SUPPORTED_LANGUAGES:
                raise NaverSTTError(f"지원하지 않는 언어입니다: {lang}")
            
            # WAV로 변환
            if format.lower() != "wav":
                audio_data = self.convert_to_wav(audio_data, format)
            
            # 오디오 파일 검증
            audio_info = self.validate_audio_file(audio_data)
            
            # API 요청 헤더 설정
            headers = {
                "X-NCP-APIGW-API-KEY-ID": self.client_id,
                "X-NCP-APIGW-API-KEY": self.client_secret,
                "Content-Type": "application/octet-stream"
            }
            
            # API 요청 파라미터 설정
            params = {
                "lang": lang
            }
            
            # API 호출
            response = requests.post(
                self.api_url,
                headers=headers,
                params=params,
                data=audio_data
            )
            
            # 응답 상태 코드 처리
            if response.status_code == 413:
                if "STT000" in response.text:
                    raise NaverSTTError("음성 데이터가 허용 용량을 초과했습니다 (최대 3MB)")
                elif "STT001" in response.text:
                    raise NaverSTTError("음성 데이터가 허용 길이를 초과했습니다 (최대 60초)")
            elif response.status_code == 400:
                if "STT002" in response.text:
                    raise NaverSTTError("잘못된 Content-Type입니다")
                elif "STT003" in response.text:
                    raise NaverSTTError("음성 데이터가 비어있습니다")
                elif "STT004" in response.text:
                    raise NaverSTTError("언어 파라미터가 입력되지 않았습니다")
                elif "STT005" in response.text:
                    raise NaverSTTError("지원하지 않는 언어입니다")
                elif "STT007" in response.text:
                    raise NaverSTTError("음성 데이터가 너무 짧습니다 (최소 400ms)")
            elif response.status_code == 500:
                if "STT006" in response.text:
                    raise NaverSTTError("음성 인식 전처리 중 오류가 발생했습니다")
                elif "STT998" in response.text:
                    raise NaverSTTError("음성 인식 중 오류가 발생했습니다")
                elif "STT999" in response.text:
                    raise NaverSTTError("내부 서버 오류가 발생했습니다")
            
            # 응답 확인
            if response.status_code == 200:
                result = response.json()
                return {
                    "text": result.get("text", ""),
                    "confidence": 1.0,  # 네이버 API는 신뢰도 점수를 제공하지 않음
                    "audio_info": audio_info
                }
            else:
                raise NaverSTTError(f"API 호출 실패: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            raise NaverSTTError(f"API 요청 중 오류가 발생했습니다: {str(e)}")
        except Exception as e:
            raise NaverSTTError(f"음성 인식 중 오류가 발생했습니다: {str(e)}") 