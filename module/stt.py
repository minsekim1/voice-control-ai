import os
from google.cloud import speech
import pyaudio

from catch_voice import execute_command


# 중복 단어 무시용 변수
transcript = ""

def initialize_client():
    # 환경변수 설정: API 키 파일 경로
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'service-account-file.json'
    # Google Cloud Speech 클라이언트 초기화
    client = speech.SpeechClient()
    return client

def listen_print_loop(responses):
    global transcript  # 글로벌 변수로 선언
    
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives or transcript == result.alternatives[0].transcript:
            continue

        # 가장 가능성 높은 대안 출력
        transcript = result.alternatives[0].transcript
        print('Transcript: {}'.format(transcript))
        if len(transcript) > 1 :
            is_command = execute_command(transcript)
            if is_command == True :
                transcript = ""

def stt_start():
    client = initialize_client()
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=2048)
    stream.start_stream()

    # 스트리밍 음성 인식 설정
    audio_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="ko-KR"
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=audio_config,
        interim_results=False
        # interim_results=True
    )

    print("BOT: 말을 시작해주세요.")
    requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in iter(lambda: stream.read(1024), b''))
    responses = client.streaming_recognize(streaming_config, requests)
    
    # 결과 처리
    listen_print_loop(responses)