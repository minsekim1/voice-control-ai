import sys
sys.path.insert(0, './module')

from PyQt5 import QtWidgets, QtCore
from transparentWindow import TransparentWindow

def onVoice():
    print("Space bar was pressed!")

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = TransparentWindow(onVoice, 40, 40)
    
    # Ctrl+C를 처리할 수 있도록 QTimer 설정
    timer = QtCore.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None) 

    app.exec_()

if __name__ == '__main__':
    main()