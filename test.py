import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QLabel, QLineEdit
import json

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("自动生成控件示例")
        self.setGeometry(100, 100, 400, 300)

        file_path, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'JSON Files (*.json)')
        if file_path:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        # 读取JSON文件
        #with open('data.json', 'r', encoding='utf-8') as f:
        #    data = json.load(f)

        # 根据JSON数据生成控件
            for item in data:
                label = QLabel(item['name'], self)
                label.move(50, 50 + 30 * item['id'])
                line_edit = QLineEdit(self)
                line_edit.move(150, 50 + 30 * item['id'])
                line_edit.setText(item['value'])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())