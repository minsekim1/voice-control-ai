import sys
import wave

import pyaudio
sys.path.insert(0, './module')

from MicController import MicController
import speech_recognition as sr


def record_audio(filename, device_index, rate, record_seconds=5, chunk_size=1024, format=pyaudio.paInt16, channels=1):
    p = pyaudio.PyAudio()

    # 스트림 열기
    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    input_device_index=device_index,
                    frames_per_buffer=chunk_size)

    print(f"Recording from device {device_index} at {rate} Hz for {record_seconds} seconds...")

    # 프레임들을 저장할 리스트
    frames = []

    # 지정된 시간 동안 오디오 데이터 읽기
    for i in range(int(rate / chunk_size * record_seconds)):
        data = stream.read(chunk_size)
        frames.append(data)

    print("Recording finished.")

    # 스트림을 멈추고 종료
    stream.stop_stream()
    stream.close()
    p.terminate()

    # WAV 파일로 저장
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"File saved: {filename}")

micController = MicController()
mic, index, rate = micController.find_uniq_active_microphone()
if mic:
    print(f"Most likely active microphone: {mic} at index {index}")
else:
    print("No active microphone found.")

# 음성 인식 시작
if mic:
    try:
        with sr.Microphone(device_index=index) as source:
            print("Listening...")
            micController.recognizer.adjust_for_ambient_noise(source, duration=1)  # 배경 소음 수준 조절
            audio = micController.recognizer.listen(source)
            record_audio("output.wav", index, rate)
            print("Recognizing...")
            text = micController.recognizer.recognize_google(audio)
            print("You said:", text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
