import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout
from pc_aeon import count_successful_pairs

class BlessingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # 创建布局
        layout = QVBoxLayout()

        # 创建行编辑框用于输入祝福数量
        self.lineEdits = [QLineEdit(self) for _ in range(9)]
        input_list = ['存护', '记忆', '虚无', '丰饶', '巡猎', '毁灭', '欢愉', '繁育', '智识']
        for i, line_edit in enumerate(self.lineEdits, 1):
            line_edit.setPlaceholderText(f'{input_list[i-1]}祝福的数量')
            layout.addWidget(line_edit)

        # 创建操作按钮
        self.button = QPushButton('执行操作', self)
        self.button.clicked.connect(self.on_button_clicked)
        layout.addWidget(self.button)

        # 设置窗口布局
        self.setLayout(layout)

        # 设置窗口标题和大小
        self.setWindowTitle('祝福数量输入')
        self.setGeometry(300, 300, 300, 200)

    def on_button_clicked(self):
        # 读取行编辑框中的值
        blessings = [int(line_edit.text()) if line_edit.text() else 0 for line_edit in self.lineEdits]
        # 调用你的操作函数（这里只是简单打印）
        count_successful_pairs(blessings)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BlessingApp()
    ex.show()
    sys.exit(app.exec_())