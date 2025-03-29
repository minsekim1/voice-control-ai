import os
from google.cloud import speech
import pyaudio
import numpy as np
from catch_voice import execute_command

# 중복 단어 무시용 변수
transcript = ""

def get_audio_devices():
    audio = pyaudio.PyAudio()
    devices = []
    for i in range(audio.get_device_count()):
        device_info = audio.get_device_info_by_index(i)
        if device_info.get('maxInputChannels') > 0:
            devices.append((i, device_info.get('name')))
    audio.terminate()
    return devices

def select_input_device():
    devices = get_audio_devices()
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

def initialize_client():
    # 환경변수 설정: API 키 파일 경로
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'service-account-file.json'
    # Google Cloud Speech 클라이언트 초기화
    client = speech.SpeechClient()
    return client

def preprocess_audio(audio_data):
    # 오디오 데이터를 numpy 배열로 변환
    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    
    # 노이즈 제거 (간단한 임계값 기반)
    threshold = 500
    audio_array[abs(audio_array) < threshold] = 0
    
    # 정규화
    max_value = np.max(np.abs(audio_array))
    if max_value > 0:
        audio_array = audio_array / max_value
    
    return audio_array.tobytes()

def listen_print_loop(responses):
    global transcript
    
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives or transcript == result.alternatives[0].transcript:
            continue

        # 가장 가능성 높은 대안 출력
        transcript = result.alternatives[0].transcript
        print('Transcript: {}'.format(transcript))
        if len(transcript) > 1:
            is_command = execute_command(transcript)
            if is_command == True:
                transcript = ""

def stt_start():
    client = initialize_client()
    audio = pyaudio.PyAudio()
    
    # 마이크 장치 선택
    input_device_index = select_input_device()
    if input_device_index is None:
        print("마이크 장치를 선택하지 않았습니다. 프로그램을 종료합니다.")
        return
    
    # 오디오 스트림 설정 최적화
    stream = audio.open(format=pyaudio.paInt16,
                       channels=1,
                       rate=16000,
                       input=True,
                       frames_per_buffer=2048,
                       input_device_index=input_device_index)
    stream.start_stream()

    # 스트리밍 음성 인식 설정 최적화
    audio_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="ko-KR",
        enable_automatic_punctuation=True,  # 자동 구두점 추가
        model="latest_long",  # 최신 장문 모델 사용
        use_enhanced=True,  # 향상된 모델 사용
        enable_word_time_offsets=True,  # 단어별 시간 정보 활성화
        enable_word_confidence=True,  # 단어별 신뢰도 점수 활성화
        enable_speaker_diarization=True  # 화자 구분 활성화
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=audio_config,
        interim_results=True  # 중간 결과도 받아옴
    )

    print("BOT: 말을 시작해주세요.")
    
    def audio_generator():
        while True:
            chunk = stream.read(1024, exception_on_overflow=False)
            processed_chunk = preprocess_audio(chunk)
            yield speech.StreamingRecognizeRequest(audio_content=processed_chunk)

    requests = audio_generator()
    responses = client.streaming_recognize(streaming_config, requests)
    
    # 결과 처리
    listen_print_loop(responses)