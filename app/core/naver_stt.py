import os
import json
import wave
import numpy as np
from ncloud.speech import SpeechClient
from ncloud.speech.model import RecognitionRequest
from ncloud.speech.model import RecognitionResponse
from ncloud.speech.model import RecognitionConfig
from ncloud.speech.model import RecognitionAudio
import base64

class NaverSTT:
    def __init__(self, access_key: str, secret_key: str):
        """
        네이버 클라우드 STT 초기화
        
        Args:
            access_key: 네이버 클라우드 액세스 키
            secret_key: 네이버 클라우드 시크릿 키
        """
        self.client = SpeechClient(access_key, secret_key)
        
    def process_audio_data(self, audio_data, sample_rate=16000):
        """오디오 데이터를 적절한 형식으로 변환합니다."""
        try:
            if isinstance(audio_data, (bytes, bytearray)):
                # WAV 파일 헤더가 있는지 확인
                if audio_data[:4] == b'RIFF' and audio_data[8:12] == b'WAVE':
                    with wave.open(io.BytesIO(audio_data), 'rb') as wf:
                        if wf.getsampwidth() != 2 or wf.getnchannels() != 1:
                            raise ValueError("Audio must be 16-bit mono")
                        audio_data = wf.readframes(wf.getnframes())
                
                # 바이트 데이터를 numpy 배열로 변환
                audio_array = np.frombuffer(audio_data, dtype=np.int16)
                
                # 음성 신호 정규화
                if np.max(np.abs(audio_array)) > 0:
                    # RMS 정규화
                    rms = np.sqrt(np.mean(np.square(audio_array)))
                    if rms > 0:
                        audio_array = np.int16(audio_array * (32767 / rms))
                
                # 샘플링 레이트 변환이 필요한 경우
                if sample_rate != 16000:
                    audio_array = librosa.resample(
                        audio_array.astype(np.float32),
                        orig_sr=sample_rate,
                        target_sr=16000
                    ).astype(np.int16)
                
                return audio_array.tobytes()
            
            return audio_data
            
        except Exception as e:
            raise Exception(f"Audio processing failed: {str(e)}")
        
    def recognize(self, audio_data, sample_rate=16000, channels=1, sample_width=2):
        """
        음성을 텍스트로 변환합니다.
        
        Args:
            audio_data: 오디오 데이터 (bytes 또는 numpy array)
            sample_rate: 샘플링 레이트 (기본값: 16000)
            channels: 채널 수 (기본값: 1)
            sample_width: 샘플 너비 (기본값: 2)
        """
        try:
            # 오디오 데이터 전처리
            processed_audio = self.process_audio_data(audio_data, sample_rate)
            
            # 오디오 데이터를 base64로 인코딩
            audio_base64 = base64.b64encode(processed_audio).decode('utf-8')
            
            # 인식 설정
            config = RecognitionConfig(
                encoding="LINEAR16",  # 16-bit PCM
                sample_rate_hertz=sample_rate,
                language_code="ko-KR",
                enable_automatic_punctuation=True,
                enable_word_time_offsets=True
            )
            
            # 오디오 데이터 설정
            audio = RecognitionAudio(
                content=audio_base64
            )
            
            # 인식 요청
            request = RecognitionRequest(
                config=config,
                audio=audio
            )
            
            # 인식 수행
            response = self.client.recognize(request)
            
            # 결과 처리
            if response and response.results:
                result = response.results[0]
                alternatives = result.alternatives
                if alternatives:
                    best_alternative = alternatives[0]
                    confidence = best_alternative.confidence
                    
                    # 단어별 신뢰도 점수 계산
                    word_confidences = []
                    for word in best_alternative.words:
                        if hasattr(word, 'confidence'):
                            word_confidences.append(word.confidence)
                    
                    if word_confidences:
                        confidence = sum(word_confidences) / len(word_confidences)
                    
                    return {
                        "text": best_alternative.transcript,
                        "confidence": confidence,
                        "params": {
                            "sample_rate": sample_rate,
                            "channels": channels,
                            "sample_width": sample_width
                        }
                    }
            
            return {
                "text": "",
                "confidence": 0.0,
                "params": {
                    "sample_rate": sample_rate,
                    "channels": channels,
                    "sample_width": sample_width
                }
            }
            
        except Exception as e:
            raise Exception(f"Recognition failed: {str(e)}") 