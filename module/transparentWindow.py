from numbers import Number
from PyQt5 import QtWidgets, QtCore, QtGui
from typing import Callable

class TransparentWindow(QtWidgets.QWidget):
    def __init__(self, onVoiceStart:Callable, onVoiceEnd: Callable, right: Number, top: Number):
        super().__init__()
        self.onVoiceStart = onVoiceStart
        self.onVoiceEnd = onVoiceEnd
        self.space_pressed = False
        self.initUI(right, top)

    def initUI(self, right: Number, top: Number):
        text = "on Voice"
        font = QtGui.QFont('Arial', 30, QtGui.QFont.Bold)

        fm = QtGui.QFontMetrics(font)
        text_width = fm.width(text)
        text_height = fm.height()

        width = text_width + 20
        height = text_height + 20

        screen = QtWidgets.QApplication.primaryScreen().geometry()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        x = screen.width() - width - right + 20
        self.setGeometry(x, top + 20, width, height)
        self.setWindowTitle('MyWindow')

        self.label = QtWidgets.QLabel(text, self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: white; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.show()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space and not self.space_pressed:
            self.label.setStyleSheet("color: red; background: transparent;")
            self.space_pressed = True
            self.onVoiceStart()
            print("Space pressed")
        elif (event.modifiers() & (QtCore.Qt.ControlModifier | QtCore.Qt.MetaModifier)) and event.key() == QtCore.Qt.Key_C:
            self.close()

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            self.label.setStyleSheet("color: white; background: transparent;")
            self.space_pressed = False
            self.onVoiceEnd()
            print("Space released")
