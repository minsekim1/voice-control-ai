from numbers import Number
from PyQt5 import QtWidgets, QtCore, QtGui
from typing import Callable

class TransparentWindow(QtWidgets.QWidget):
    def __init__(self, onVoice: Callable, right: Number, top: Number):
        super().__init__()
        self.onVoice = onVoice
        self.space_pressed = False
        self.initUI(right, top)

    def initUI(self, right: Number, top: Number):
        # 사용할 텍스트와 폰트 설정
        text = "on Voice"
        font = QtGui.QFont('Arial', 30, QtGui.QFont.Bold)

        # QFontMetrics를 사용하여 텍스트 크기 측정
        fm = QtGui.QFontMetrics(font)
        text_width = fm.width(text)
        text_height = fm.height()

        # 윈도우 너비와 높이를 텍스트 크기에 맞게 설정
        width = text_width + 20  # 텍스트 양 옆에 여백 추가
        height = text_height + 20  # 텍스트 위아래에 여백 추가

        # 화면 해상도 얻기
        screen = QtWidgets.QApplication.primaryScreen().geometry()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 윈도우 위치 설정
        x = screen.width() - width - right + 20  # 오른쪽에서 100px 떨어진 위치

        # 윈도우 위치와 크기 설정
        self.setGeometry(x, top + 20, width, height)
        self.setWindowTitle('MyWindow')

        # 라벨 설정
        self.label = QtWidgets.QLabel(text, self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: white; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.show()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space and not self.space_pressed:
            self.label.setStyleSheet("color: red; background: transparent;")
            self.onVoice()
            self.space_pressed = True
        elif (event.modifiers() & (QtCore.Qt.ControlModifier | QtCore.Qt.MetaModifier)) and event.key() == QtCore.Qt.Key_C:
            self.close()

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            self.label.setStyleSheet("color: white; background: transparent;")
            self.space_pressed = False
