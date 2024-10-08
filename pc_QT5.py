import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(500, 500)
        self.move(300, 300)
        self.setWindowTitle('JulyStone')
        self.setWindowIcon(QIcon('./pics/flag.png'))
        layout = QVBoxLayout()
        btn1 = QPushButton('Button1', self)
        layout.addWidget(btn1)
        btn2 = QPushButton('Button2', self)
        layout.addWidget(btn2)
        btn3 = QPushButton('Button3', self)
        layout.addWidget(btn3)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWindow()

    w.show()
    app.exec_()
