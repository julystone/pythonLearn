# encoding: utf-8

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, \
    QWidget, QHBoxLayout
from pc_readCVM import cvm_2_obj
from pc_readCVM_2 import rule_2_obj


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # self.resize(300, 200)
        self.setWindowTitle('腾讯云excel文件处理器')

        # 创建布局和控件
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)
        layout_head = QHBoxLayout(self.central_widget)
        layout_mid = QHBoxLayout(self.central_widget)
        layout_tail = QHBoxLayout(self.central_widget)

        self.excel_folder_label = QLabel('选择待处理文件所在位置:', self)
        self.excel_folder_entry = QLineEdit(self)
        self.excel_folder_button = QPushButton('选择文件夹', self)
        self.excel_folder_button.clicked.connect(self.select_excel_folder)

        self.obj_file_label = QLabel('选择统计归档的文件:', self)
        self.obj_file_entry = QLineEdit(self)
        self.obj_file_button = QPushButton('选择文件', self)
        self.obj_file_button.clicked.connect(self.select_obj_file)

        self.transfer_cvm_button = QPushButton('cvm拼接', self)
        self.transfer_cvm_button.clicked.connect(self.transfer_cvm)

        self.merge_rules_button = QPushButton('ins_rules表合并', self)
        self.merge_rules_button.clicked.connect(self.merge_rule)

        # 添加到布局中
        layout.addWidget(self.excel_folder_label)
        layout_head.addWidget(self.excel_folder_entry)
        layout_head.addWidget(self.excel_folder_button)
        layout.addLayout(layout_head)
        layout.addWidget(self.obj_file_label)
        layout_mid.addWidget(self.obj_file_entry)
        layout_mid.addWidget(self.obj_file_button)
        layout.addLayout(layout_mid)
        layout_tail.addWidget(self.transfer_cvm_button)
        layout_tail.addWidget(self.merge_rules_button)
        layout.addLayout(layout_tail)

        # self.setLayout(layout)
        self.show()

    def select_excel_folder(self):
        folder_selected = QFileDialog.getExistingDirectory(self, "选择待处理文件所在位置")
        if folder_selected:
            self.excel_folder_entry.setText(folder_selected)

    def select_obj_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择统计归档文件", "", "Excel Files (*.xlsx)")
        if file_path:
            self.obj_file_entry.setText(file_path)

    def transfer_cvm(self):
        excel_folder = self.excel_folder_entry.text()
        obj_file = self.obj_file_entry.text()
        cvm_2_obj(excel_folder, obj_file, "腾讯云成都")

    def merge_rule(self):
        excel_folder = self.excel_folder_entry.text()
        rule_2_obj(excel_folder)


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = MainWindow()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"An error occured: {e}")
