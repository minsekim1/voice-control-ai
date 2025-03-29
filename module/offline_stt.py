import wave
import json
import pyaudio
import os
from vosk import Model, KaldiRecognizer

class OfflineSTT:
    def __init__(self):
        # Vosk 모델 경로 설정
        model_path = "vosk-model-ko"
        if not os.path.exists(model_path):
            print("한국어 Vosk 모델을 다운로드해야 합니다.")
            print("https://alphacephei.com/vosk/models 에서 vosk-model-ko를 다운로드하세요.")
            return
        
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        
        # PyAudio 설정
        self.audio = pyaudio.PyAudio()
        self.stream = None
        
    def get_audio_devices(self):
        devices = []
        for i in range(self.audio.get_device_count()):
            device_info = self.audio.get_device_info_by_index(i)
            if device_info.get('maxInputChannels') > 0:
                devices.append((i, device_info.get('name')))
        return devices
        
    def select_input_device(self):
        devices = self.get_audio_devices()
        if not devices:
            print("사용 가능한 마이크 장치가 없습니다.")
            return None
            
        print("\n사용 가능한 마이크 장치:")
        for i, (device_id, name) in enumerate(devices):
            print(f"{i+1}. {name} (ID: {device_id})")
        
        while True:
            try:
                choice = int(input("\n사용할 마이크 장치 번호를 선택하세요: ")) - 1
                if 0 <= choice < len(devices):
                    return devices[choice][0]
                print("잘못된 선택입니다. 다시 선택해주세요.")
            except ValueError:
                print("숫자를 입력해주세요.")
        
    def start_recording(self):
        # 마이크 장치 선택
        input_device_index = self.select_input_device()
        if input_device_index is None:
            print("마이크 장치를 선택하지 않았습니다.")
            return False
            
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=2048,
            input_device_index=input_device_index
        )
        self.stream.start_stream()
        print("오프라인 음성 인식 시작...")
        return True
        
    def stop_recording(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
            print("오프라인 음성 인식 종료")
            
    def process_audio(self):
        if not self.stream:
            return None
            
        data = self.stream.read(2048, exception_on_overflow=False)
        if self.recognizer.AcceptWaveform(data):
            result = json.loads(self.recognizer.Result())
            if result.get("text", "").strip():
                return result["text"]
        return None
        
    def close(self):
        self.stop_recording()
        self.audio.terminate()
        
def offline_stt_start():
    stt = OfflineSTT()
    try:
        if not stt.start_recording():
            return
        while True:
            text = stt.process_audio()
            if text:
                print(f"오프라인 인식 결과: {text}")
                # 여기에 명령어 처리 로직 추가
    except KeyboardInterrupt:
        print("\n프로그램 종료")
    finally:
        stt.close() 