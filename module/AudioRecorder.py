import pyaudio
import wave
import os
import sys
from PyQt5 import QtCore, QtWidgets
from uuid import uuid4

from PythonSpeechRecognition import PythonSpeechRecognition

class AudioRecorder:
    def __init__(self, filename="output.wav", format=pyaudio.paInt16, channels=1, rate=44100, chunk=2048, input_device_index=None):
        self.filename = filename
        self.format = format
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.input_device_index = input_device_index
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.record_chunk)

        self.exit_timer = QtCore.QTimer()
        self.exit_timer.start(500)
        self.exit_timer.timeout.connect(lambda: None) 

    def get_inputs_list(self):
        info = self.audio.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        input_devices = []

        for i in range(numdevices):
            device_info = self.audio.get_device_info_by_host_api_device_index(0, i)
            if device_info.get('maxInputChannels') > 0:
                input_devices.append({
                    "index": i,
                    "name": device_info.get('name')
                })
                print(f"Input Available Device {i}: {device_info.get('name')}, Input Channels: {device_info.get('maxInputChannels')}")

        return input_devices

    def start_recording(self, input_device_index=None):
        if input_device_index is not None:
            self.input_device_index = input_device_index

        # 기존 파일 삭제
        if os.path.exists(self.filename):
            os.remove(self.filename)
            print(f"Deleted existing file: {self.filename}")

        try:
            self.stream = self.audio.open(format=self.format,
                                          channels=self.channels,
                                          rate=self.rate,
                                          input=True,
                                          input_device_index=self.input_device_index,
                                          frames_per_buffer=self.chunk)
            self.frames = []
            print("Recording started")
        except Exception as e:
            print(f"Failed to start recording: {e}")
            self.stream = None

    def stop_recording(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

        if self.frames:
            try:
                with wave.open(self.filename, 'wb') as wf:
                    wf.setnchannels(self.channels)
                    wf.setsampwidth(self.audio.get_sample_size(self.format))
                    wf.setframerate(self.rate)
                    wf.writeframes(b''.join(self.frames))
                print(f"Recording stopped, saved to {self.filename}")
            except Exception as e:
                print(f"Failed to save recording: {e}")

    def record_chunk(self):
        if self.stream:
            try:
                data = self.stream.read(self.chunk, exception_on_overflow=False)
                self.frames.append(data)
                print(f"Recording chunk, total frames: {len(self.frames)}")
            except Exception as e:
                print(f"Error recording chunk: {e}")

    def terminate(self):
        self.audio.terminate()

    def onVoiceStart(self):
        print("Start")
        input_list = self.get_inputs_list()
        if len(input_list) == 0:
            print("ERR: no input device")
            return
        
        input_index = 3
        input_device = input_list[input_index]['index']
        self.start_recording(input_device)
        self.timer.start(1)  # 100ms마다 chunk를 기록하도록 타이머 시작
        print("Timer started")

    def onVoiceEnd(self):
        print("END")
        self.stop_recording()
        self.timer.stop()
        
        #옵션1 GoogleCloudSpeech를 사용하여 녹음된 파일을 텍스트로 변환
        # credentials_path = "./service-account-file.json"  # 실제 자격 증명 파일 경로로 변경
        # transcriber = GoogleCloudSpeech(credentials_path)
        # transcription = transcriber.get_transcription("output.wav")
        # print("Transcription:", transcription)

        #옵션2 PythonSpeechRecognition을 사용하여 녹음된 파일을 텍스트로 변환
        transcriber = PythonSpeechRecognition()
        transcription = transcriber.transcribe_audio("output.wav")
        print("Transcription:", transcription)

    def record_chunk(self):
        if self.stream:
            try:
                data = self.stream.read(self.chunk, exception_on_overflow=False)
                self.frames.append(data)
                print(f"Recording chunk, total frames: {len(self.frames)}")
            except Exception as e:
                print(f"Error recording chunk: {e}")