import json
import wave
import numpy as np
from vosk import Model, KaldiRecognizer
import os

class VoskSTT:
    def __init__(self, model_path="model/vosk-model-small-ko-0.22"):
        """
        Vosk STT 초기화
        """
        if not os.path.exists(model_path):
            raise ValueError(f"모델 경로를 찾을 수 없습니다: {model_path}")
            
        self.model = Model(model_path)
        self.rec = KaldiRecognizer(self.model, 16000)
        
    def recognize(self, audio_data):
        """
        오디오 데이터를 텍스트로 변환
        """
        if self.rec.AcceptWaveform(audio_data):
            result = json.loads(self.rec.Result())
            return {
                "text": result.get("text", ""),
                "confidence": result.get("confidence", 0.0)
            }
        else:
            # 부분 결과 반환
            result = json.loads(self.rec.PartialResult())
            return {
                "text": result.get("partial", ""),
                "confidence": 0.0
            }
            
    def reset(self):
        """
        인식기 상태 초기화
        """
        self.rec = KaldiRecognizer(self.model, 16000) 