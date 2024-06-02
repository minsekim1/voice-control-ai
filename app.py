import sys
sys.path.insert(0, './module')

from PyQt5 import QtWidgets, QtCore
from TransparentWindow import TransparentWindow
from AudioRecorder import AudioRecorder

# 적절한 입력 장치 인덱스를 설정합니다. (예: 1번 장치)
input_device_index = 1
recorder = AudioRecorder(input_device_index=input_device_index)

def onVoiceStart():
    print("Start")
    input_list = recorder.get_inputs_list()
    if(len(input_list) == 0):
        print("ERR: no input device")
        return
    
    input_dvice = input_list[0]['index']
    recorder.start_recording(input_dvice)
    timer.start(100)  # 100ms마다 chunk를 기록하도록 타이머 시작

def onVoiceEnd():
    print("END")
    recorder.stop_recording()
    timer.stop()

def record_chunk():
    recorder.record_chunk()

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = TransparentWindow(onVoiceStart, onVoiceEnd, 40, 40)
    
    global timer  # 타이머를 글로벌로 정의하여 여러 함수에서 접근 가능하도록 함
    timer = QtCore.QTimer()
    timer.timeout.connect(record_chunk)

    # Ctrl+C를 처리할 수 있도록 QTimer 설정
    exit_timer = QtCore.QTimer()
    exit_timer.start(500)
    exit_timer.timeout.connect(lambda: None) 

    app.exec_()

if __name__ == '__main__':
    main()
