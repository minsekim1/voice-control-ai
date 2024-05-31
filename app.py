from PyQt5 import QtWidgets, QtCore, QtGui

class TransparentWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 400, 200)  # 창 위치와 크기 설정

        layout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel("on Voice", self)
        self.label.setFont(QtGui.QFont('Arial', 30, QtGui.QFont.Bold))
        self.label.setStyleSheet("color: white; background: transparent;")
        
        # 텍스트에 그림자 효과 추가
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QtGui.QColor('black'))
        shadow.setOffset(1, 1)
        self.label.setGraphicsEffect(shadow)

        layout.addWidget(self.label)

        self.setLayout(layout)
        self.show()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            self.label.setStyleSheet("color: red; background: transparent;")
        elif (event.modifiers() & (QtCore.Qt.ControlModifier | QtCore.Qt.MetaModifier)) and event.key() == QtCore.Qt.Key_C:
            self.close()

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            self.label.setStyleSheet("color: white; background: transparent;")

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    ex = TransparentWindow()
    app.exec_()
