import sys

from GoogleCloudSpeech import GoogleCloudSpeech
sys.path.insert(0, './module')

from PyQt5 import QtWidgets, QtCore
from TransparentWindow import TransparentWindow
from AudioRecorder import AudioRecorder

recorder = AudioRecorder()

def onVoiceStart():
    print("Start")
    input_list = recorder.get_inputs_list()
    if len(input_list) == 0:
        print("ERR: no input device")
        return
    
    input_device = input_list[0]['index']
    recorder.start_recording(input_device)
    timer.start(10)  # 10ms마다 chunk를 기록하도록 타이머 시작
    print("Timer started")

def onVoiceEnd():
    print("END")
    recorder.stop_recording()
    timer.stop()
    
    # GoogleCloudSpeech를 사용하여 녹음된 파일을 텍스트로 변환
    transcriber = GoogleCloudSpeech()
    transcription = transcriber.get_transcription("output.wav")
    print("Transcription:", transcription)

def record_chunk():
    recorder.record_chunk()

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = TransparentWindow(onVoiceStart, onVoiceEnd, 40, 40)
    
    global timer
    timer = QtCore.QTimer()
    timer.timeout.connect(record_chunk)

    exit_timer = QtCore.QTimer()
    exit_timer.start(500)
    exit_timer.timeout.connect(lambda: None) 

    app.exec_()
    recorder.terminate()

if __name__ == '__main__':
    main()
