import json
import wave
import numpy as np
from vosk import Model, KaldiRecognizer
import os
import io
import librosa

class VoskSTT:
    def __init__(self, model_path="model/vosk-model-small-ko-0.22"):
        """
        Vosk STT 초기화
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")
            
        self.model = Model(model_path)
        self.reset()
        
    def reset(self):
        """인식기 상태를 초기화합니다."""
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.recognizer.SetWords(True)
        
    def process_audio_data(self, audio_data, sample_rate=16000):
        """오디오 데이터를 적절한 형식으로 변환합니다."""
        if isinstance(audio_data, (bytes, bytearray)):
            # WAV 파일 헤더가 있는지 확인
            if audio_data[:4] == b'RIFF' and audio_data[8:12] == b'WAVE':
                with wave.open(io.BytesIO(audio_data), 'rb') as wf:
                    if wf.getsampwidth() != 2 or wf.getnchannels() != 1:
                        raise ValueError("Audio must be 16-bit mono")
                    audio_data = wf.readframes(wf.getnframes())
            
            # 바이트 데이터를 numpy 배열로 변환
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            
            # 샘플링 레이트 변환이 필요한 경우
            if sample_rate != 16000:
                audio_array = librosa.resample(
                    audio_array.astype(np.float32),
                    orig_sr=sample_rate,
                    target_sr=16000
                ).astype(np.int16)
                
            return audio_array.tobytes()
        
        return audio_data
        
    def recognize(self, audio_data, sample_rate=16000):
        """음성을 텍스트로 변환합니다."""
        try:
            # 오디오 데이터 전처리
            processed_audio = self.process_audio_data(audio_data, sample_rate)
            
            # 인식 수행
            if self.recognizer.AcceptWaveform(processed_audio):
                result = json.loads(self.recognizer.Result())
            else:
                result = json.loads(self.recognizer.PartialResult())
            
            # 인식기 초기화
            self.reset()
            
            return {
                "text": result.get("text", ""),
                "confidence": result.get("confidence", 0.0)
            }
            
        except Exception as e:
            self.reset()  # 오류 발생 시에도 초기화
            raise Exception(f"Recognition failed: {str(e)}") 