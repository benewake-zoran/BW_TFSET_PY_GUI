import sys
import json
import serial
import serial.tools.list_ports
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import QFile, QTextStream
from Ui_WINCC import Ui_MainWindow


class MyMainWindow(QMainWindow, Ui_MainWindow):  # 继承QMainWindow类和Ui_Maindow界面类
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)  # 初始化父类
        self.setupUi(self)  # 继承 Ui_MainWindow 界面类

    def getSerialPort(self):
        ports = serial.tools.list_ports.comports()
        if len(ports) == 0:
            self.comboBox.addItem("-- 无串口 --")
        else:
            for port in ports:
                self.comboBox.addItem(port.device)

    def connectSerial(self):
        self.ser = serial.Serial()
        select_port = self.comboBox.currentText()  # 获取串口下拉列表值
        self.ser.port = select_port
        self.ser.baudrate = self.comboBox_2.currentText()  # 获取波特率值
        self.ser.open()
        self.ser.reset_input_buffer()
        print('seclect port is:', select_port)
        print('baudrate is:', self.ser.baudrate)

    def trigger_actOpen(self):
        # 打开文件对话框
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'JSON Files (*.json)')
        if file_path:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)

            Cmdlist = []  # 指令保存列表
            self.buttons = []  # 按钮列表
            # 根据JSON数据生成控件
            layout = QtWidgets.QGridLayout()
            layout.setColumnStretch(0, 1)  # 第一列宽度自适应
            layout.setColumnStretch(1, 3)  # 第二列宽度自适应
            layout.setColumnStretch(2, 1)  # 第三列宽度为第二列的两倍
            for item in self.data:
                Cmdlist.append(item['cmd'])  # 指令保存
                print('cmd:', item['cmd'], item['id'])

                label = QtWidgets.QLabel(item['name'], self)
                layout.addWidget(label, item['id'], 0)
                if item['widget'] == 'QLabel':
                    widget = QtWidgets.QLabel(self)
                    if item['name'] == '保存' or item['name'] == '恢复出厂':
                        widget.setText('---')
                        widget.setAlignment(QtCore.Qt.AlignCenter)
                    layout.addWidget(widget, item['id'], 1)
                elif item['widget'] == 'QComboBox':
                    widget = QtWidgets.QComboBox(self)
                    widget.addItems(["标准9字节(cm)", "字符串格式(m)", "标准9字节(mm)"])
                    layout.addWidget(widget, item['id'], 1)
                elif item['widget'] == 'QLineEdit':
                    widget = QtWidgets.QLineEdit(self)
                    widget.setPlaceholderText("1 - 1000 (Hz)")
                    layout.addWidget(widget, item['id'], 1)
                else:
                    widget = QtWidgets.QLabel(item['widget'], self)

                button = QtWidgets.QPushButton(item['button'], self)
                layout.addWidget(button, item['id'], 2)
                self.buttons.append(button)

            print('list:', Cmdlist)
            print('buttons:', self.buttons)
            self.centralwidget.setLayout(layout)
            # 连接指令按钮的点击信号和槽函数
            for button in self.buttons:
                button.clicked.connect(self.sendCmd)
            '''
            button = self.sender()  # 获取当前被点击的按钮
            index = self.buttons.index(button)  # 获取按钮在列表中的索引
            cmd = self.data[index]['cmd']  # 获取对应的指令
            print('send cmd:', cmd)
            self.ser.write(cmd.encode())  # 发送指令
            '''
        '''
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Text Files (*.txt)')
        if file_path:
            # 读取文件内容并显示在文本框中
            with open(file_path, 'r', encoding='utf-8') as f:
                fileContent = f.read()
                self.textEdit.setText(fileContent)
        '''

    def saveCmd(self):
        # 打开文件对话框
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'JSON Files (*.json)')
        if file_path:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            Cmdlist = []
            for item in data:
                Cmdlist.append(item['cmd'])

                print('cmd:', item['cmd'], item['id'])
            print('list:', Cmdlist)

    def sendCmd(self):
        #self.ser.write()
        self.ser.reset_input_buffer()
        button = self.sender()  # 获取当前被点击的按钮
        index = self.buttons.index(button)  # 获取按钮在列表中的索引
        cmd = self.data[index]['cmd']  # 获取对应的指令
        print('send cmd:', cmd)
        cmdb = bytes.fromhex(cmd)
        print(cmdb)
        self.ser.write(cmdb)  # 发送指令
        #rx = self.ser.read(7)
        #print('rx:',rx)
        #print('rxh:',rx.hex())


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建应用程序对象
    myWin = MyMainWindow()  # 实例化 MyMainWindow 类，创建主窗口
    myWin.show()  # 在桌面显示控件 myWin
    myWin.getSerialPort()  # 获取串口列表
    #myWin.saveCmd()
    #myWin.sendCmd() 
    sys.exit(app.exec_())  # 在主线程中退出
