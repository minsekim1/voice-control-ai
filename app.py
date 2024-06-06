import sys
sys.path.insert(0, './module')

from PyQt5 import QtWidgets
from TransparentWindow import TransparentWindow
from AudioRecorder import AudioRecorder

def main():
    recorder = AudioRecorder()

    app = QtWidgets.QApplication(sys.argv)
    ex = TransparentWindow(recorder.onVoiceStart, recorder.onVoiceEnd, 40, 40)
    
    app.exec_()
    recorder.terminate()

if __name__ == '__main__':
    main()
