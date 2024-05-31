from PyQt5 import QtWidgets, QtCore, QtGui

class TransparentWindow(QtWidgets.QWidget):
    def __init__(self, onVoice):
        super().__init__()
        self.onVoice = onVoice
        self.space_pressed = False
        self.initUI()
    
    def initUI(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 400, 200)

        layout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel("on Voice", self)
        self.label.setFont(QtGui.QFont('Arial', 30, QtGui.QFont.Bold))
        self.label.setStyleSheet("color: white; background: transparent;")
        
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QtGui.QColor('black'))
        shadow.setOffset(1, 1)
        self.label.setGraphicsEffect(shadow)

        layout.addWidget(self.label)
        self.setLayout(layout)
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
