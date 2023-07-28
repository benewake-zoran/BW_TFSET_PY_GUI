import sys
import json
import time
import os
import datetime
import serial
import serial.tools.list_ports
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import QTimer, QTranslator
from PyQt5.QtGui import QFont
from Ui_WINCC import Ui_MainWindow
import func.UART


class MyMainWindow(QMainWindow, Ui_MainWindow):  # 继承QMainWindow类和Ui_Maindow界面类
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)  # 初始化父类
        self.setupUi(self)  # 继承 Ui_MainWindow 界面类
        self.namelist = []  # 初始化点击按钮对应操作名称的列表
        self.vallist = []  # 初始化点击按钮对应显示值的列表
        self.returnlist = []  # 初始化点击按钮对应操作结果的列表
        self.cmdlist = []  # 初始化点击按钮对应发送指令的列表
        self.rxlist = []  # 初始化点击按钮对应接收指令的列表
        self.lineEdit_id.setHidden(True)
        self.label_id.setHidden(True)

    # 获取串口列表
    def getSerialPort(self):
        ports = serial.tools.list_ports.comports()
        if len(ports) == 0:
            self.comboBox_serial.addItem("None")
            self.pushButton_connect.setEnabled(False)
        else:
            for port in reversed(ports):
                self.comboBox_serial.addItem(port.device)

    # 接口下拉列表改变时从机地址输入框变化
    def comboBoxPortChange(self):
        if self.comboBox_port.currentText() == 'UART' or self.comboBox_port.currentText() == 'RS232':
            self.lineEdit_id.setHidden(True)
            self.label_id.setHidden(True)
        if self.comboBox_port.currentText() == 'IIC':
            self.label_id.setHidden(False)
            self.lineEdit_id.setHidden(False)
            self.lineEdit_id.setPlaceholderText("0x01-0x7F")
        elif self.comboBox_port.currentText() == 'RS485':
            self.label_id.setHidden(False)
            self.lineEdit_id.setHidden(False)            
            self.lineEdit_id.setPlaceholderText("0x01-0xF7")

    # 连接按钮的信号和槽函数
    def connectSerial(self):
        try:
            self.ser = serial.Serial()
            select_port = self.comboBox_serial.currentText()  # 获取串口下拉列表值
            self.ser.port = select_port
            self.ser.baudrate = self.comboBox_baudrate.currentText()  # 获取波特率值
            self.ser.timeout = 2
            self.ser.setRTS(False)  # 禁用RTS信号(IIC通信要禁用)
            self.ser.setDTR(False)
            self.ser.open()
            print('seclect port is:', select_port)
            print('baudrate is:', self.ser.baudrate)
            # 串口连接按钮状态转换
            if self.pushButton_connect.text() == '连接串口':
                self.pushButton_connect.setText('已连接')
                self.pushButton_connect.setStyleSheet("background-color: yellow")
                self.comboBox_serial.setDisabled(True)
                self.comboBox_baudrate.setDisabled(True)
                self.comboBox_port.setDisabled(True)
                self.lineEdit_id.setDisabled(True)
                print('serial port is open')
            else:
                self.pushButton_connect.setText('连接串口')
                self.pushButton_connect.setStyleSheet("background-color: none")
                self.comboBox_serial.setDisabled(False)
                self.comboBox_baudrate.setDisabled(False)
                self.comboBox_port.setDisabled(False)
                self.lineEdit_id.setDisabled(False)
                self.ser.close()
                print('serial port is close')
            print('------------------------------')
            self.clearLabel()
        except Exception as e:
            print(type(e))
            print(e)
            if type(e) == serial.serialutil.SerialException:
                QMessageBox.warning(self, '提示', '串口无法打开，请检查！\n1.可能串口松了\n2.可能被其他程序占用\n3.转接板不支持当前波特率')

    # 刷新按钮的信号和槽函数
    def refreshSerial(self):
        try:
            self.pushButton_connect.setEnabled(True)
            self.comboBox_serial.clear()
            myWin.getSerialPort()  # 获取串口列表
            if self.pushButton_connect.text() == '已连接':
                self.pushButton_connect.setText('连接串口')
                self.pushButton_connect.setStyleSheet("background-color: none")
                self.comboBox_serial.setDisabled(False)
                self.comboBox_baudrate.setDisabled(False)
                self.comboBox_port.setDisabled(False)
                self.lineEdit_id.setDisabled(False)
                if self.comboBox_port.currentText() == 'IIC':
                    func.IIC.refresh_IIC(self)  # 复位IIC转接板
                self.ser.close()
                print('serial port is close')
            print('refresh serial port')
            print('------------------------------')
            self.clearLabel()
        except Exception as e:
            print(type(e))
            print(e)

    # 菜单栏打开的信号和槽函数
    def trigger_actOpen(self):
        try:
            # 打开文件对话框
            file_path, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'JSON Files (*.json)')
            if file_path:
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)

                Cmdlist = []  # 指令保存列表
                self.labellist = []  # 标签名称列表
                self.widgetslist = []  # 组件列表
                self.buttonlist = []  # 按钮列表
                self.labelReturnlist = []  # 结果返回OK/NG标签列表

                # 根据JSON数据生成控件
                layout = QtWidgets.QGridLayout()
                layout.setColumnStretch(0, 1)  # 第一列宽度设置为1
                layout.setColumnStretch(1, 4)  # 第二列宽度设置为3
                layout.setColumnStretch(2, 1)  # 第三列宽度设置为1
                # layout.setColumnStretch(3, 1)  # 第四列宽度设置为1

                for item in self.data:
                    Cmdlist.append(item['cmd'])  # 指令保存
                    print('cmd:', item['cmd'], item['id'])
                    # 自动保存name为QLabel
                    labelName = QtWidgets.QLabel(item['name'], self)
                    layout.addWidget(labelName, item['id'], 0)  # 第一列为配置项的名称
                    self.labellist.append(labelName)
                    # 自动保存widget为各个类型
                    if item['widget'] == 'QLabel':
                        widget = QtWidgets.QLabel(self)
                        widget.setAlignment(QtCore.Qt.AlignCenter)
                        layout.addWidget(widget, item['id'], 1)  # 第二列为不同类型组件
                    elif item['widget'] == 'QComboBox':
                        widget = QtWidgets.QComboBox(self)
                        if item['name'] == '输出模式':
                            widget.addItems(["标准9字节(cm)", "字符串格式(m)", "标准9字节(mm)"])
                        elif item['name'] == '波特率':
                            widget.addItems(['9600', '19200', '38400', '57600', '115200', '256000', '460800', '921600'])
                        elif item['name'] == '输出开关':
                            widget.addItems(['关闭数据输出', '使能数据输出'])
                        elif item['name'] == '通信接口设置':
                            widget.addItems(['UART', 'I2C'])
                        elif item['name'] == '获取测距结果':
                            widget.addItems(['数据帧(标准9字节(cm))', '数据帧(标准9字节(mm))'])
                        else:
                            widget.setEditable(True)
                        layout.addWidget(widget, item['id'], 1)  # 第二列为不同类型组件
                    elif item['widget'] == 'QLineEdit':
                        widget = QtWidgets.QLineEdit(self)
                        if item['name'] == '输出帧率':
                            widget.setPlaceholderText("0 - 1000")
                        elif item['name'] == '修改I2C从机地址':
                            widget.setPlaceholderText("0x01 - 0x7F")
                        elif item['name'] == 'I/O模式使能':
                            widget.setPlaceholderText("eg:0 100 10 (DEC)")
                        elif item['name'] == '低功耗模式使能':
                            widget.setPlaceholderText("0(关闭);1 - 10 (打开)")
                        elif item['name'] == '强度低阈值和输出':
                            widget.setPlaceholderText("eg:100 1200 (DEC)")
                        layout.addWidget(widget, item['id'], 1)  # 第二列为不同类型组件
                    else:
                        print('widget is False')
                    self.widgetslist.append(widget)  # 将组件对象添加到组件列表中

                    # 自动保存button为QPushButton
                    button = QtWidgets.QPushButton(item['button'], self)  # 构造一个QPushButton对象，item['button']是按钮的文本，self是QWidget类型，表示父组件
                    layout.addWidget(button, item['id'], 2)  # 添加的控件对象为button，控件所在的行号为item['id']，控件所在的列号为2
                    self.buttonlist.append(button)  # 将按钮对象添加到按钮列表中
                    # 自动在按钮后添加一个返回QLabel
                    labelReturn = QtWidgets.QLabel('      ', self)  # 构造一个QLabel对象，'OK'是按钮的文本，self是QWidget类型，表示父组件
                    labelReturn.setFont(QFont("Arial", 8, QFont.Bold))  # 设置字体并加粗
                    layout.addWidget(labelReturn, item['id'], 3)  # 添加的控件对象为labelReturn，控件所在的行号为item['id']，控件所在的列号为3
                    self.labelReturnlist.append(labelReturn)  # 将标签对象添加到标签列表中

                print('Cmdlist:', Cmdlist)
                print('labellist:', self.labellist)
                print('widgetslist:', self.widgetslist)
                print('buttonlist:', self.buttonlist)
                print('labelReturnlist:', self.labelReturnlist)
                print('------------------------------')

                if not self.widget1.layout():
                    self.widget1.setLayout(layout)
                else:
                    QtWidgets.QWidget().setLayout(self.widget1.layout())  # 清除原有布局
                    self.widget1.setLayout(layout)  # 设置新布局

                # 连接指令按钮的点击信号和槽函数
                for button in self.buttonlist:
                    button.clicked.connect(self.sendCmd)
                    self.timer = QTimer(self)
                    self.timer.timeout.connect(self.blinkLabel)  # 计时器结束调用闪烁标签效果
        except Exception as e:
            print(type(e))
            print(e)

    # 根据点击按钮的索引发送不同的指令
    def sendCmd(self):
        try:
            button = self.sender()  # 获取当前被点击的按钮
            self.index = self.buttonlist.index(button)  # 获取按钮在列表中的索引
            if self.comboBox_port.currentText() == 'UART':
                func.UART.send_UART(self)
                func.UART.recvData_UART(self)
                if self.rx != b'':
                    func.UART.nameType_UART(self)

            self.timer.start(100)  # 启动计时器为100毫秒
            self.savelist()
            self.saveSetting()

        except Exception as e:
            print(e)
            print(type(e))
            self.labelReturnlist[self.index].setText('NG')
            self.labelReturnlist[self.index].setStyleSheet('color: red')
            if self.data[self.index]['widget'] == 'QLabel':
                self.widgetslist[self.index].setText('')
            if type(e) == AttributeError or type(e) == serial.serialutil.PortNotOpenError:
                QMessageBox.warning(None, 'Error', '串口未连接或读取数据失败！')
            elif type(e) == ValueError or type(e) == IndexError:
                if self.data[self.index]['widget'] != 'QLabel':
                    QMessageBox.warning(None, 'Error', '检查输入值！')
            else:
                QMessageBox.warning(None, 'Error', str(e))

    # 清除组件标签内容以及返回标签内容
    def clearLabel(self):
        for widgetlabel in self.widgetslist:
            if type(widgetlabel) == QtWidgets.QLabel:
                widgetlabel.setText('')
        for returnlabel in self.labelReturnlist:
            returnlabel.setText('      ')

    # 计时器停止后，切换标签的可见性来实现闪烁效果
    def blinkLabel(self):
        if self.widgetslist[self.index].isVisible() and self.labelReturnlist[self.index].isVisible():
            self.widgetslist[self.index].setVisible(False)
            self.labelReturnlist[self.index].setVisible(False)
        else:
            self.widgetslist[self.index].setVisible(True)
            self.labelReturnlist[self.index].setVisible(True)
            self.timer.stop()

    # 保存每次点击按钮收发的数据为列表
    def savelist(self):
        self.namelist.append(self.data[self.index]['name'])
        self.returnlist.append(self.labelReturnlist[self.index].text())
        self.rxlist.append(' '.join([hex(x)[2:].zfill(2) for x in self.rx]))
        if self.data[self.index]['widget'] == 'QLabel':
            self.vallist.append(self.widgetslist[self.index].text())
            self.cmdlist.append(self.data[self.index]['cmd'])
        elif self.data[self.index]['widget'] == 'QLineEdit':
            self.vallist.append(self.widgetslist[self.index].text())
            self.cmdlist.append(' '.join([hex(x)[2:].zfill(2) for x in self.newCmd]))
        elif self.data[self.index]['widget'] == 'QComboBox':
            self.vallist.append(self.widgetslist[self.index].currentText())
            self.cmdlist.append(' '.join([hex(x)[2:].zfill(2) for x in self.newCmd]))
        print(self.namelist, self.vallist, self.returnlist, self.cmdlist, self.rxlist)

    # 保存每次设置的数据到txt文档中
    def saveSetting(self):
        # 定义txt文件名
        file_name = '{:03d}.txt'.format(self.lentxt + 1)
        # 定义待保存的文件路径（在新建的文件夹下）
        file_path = os.path.join(self.dir_path, file_name)
        # 打开文件写入数据
        with open(file_path, 'w') as f:
            for i in range(len(self.namelist)):
                f.write(self.namelist[i] + ': ' + self.vallist[i] + '    结果: ' + self.returnlist[i] + '\n' +
                        '发送cmd: ' + self.cmdlist[i].upper() + '\n' + '接收cmd: ' + self.rxlist[i].upper() + '\n' +
                        '------------------------------' + '\n')
        f.close()

    # 创建以当前日期命名的文件夹，检查当前目录下的txt文档，并获取要创建的txt文档的名称
    def gettxtname(self):
        # 获取当前日期，作为文件夹名字
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        # 定义待保存的文件夹路径（在程序目录下）
        self.dir_path = os.path.join(os.getcwd(), today)
        # 如果文件夹不存在，则创建文件夹
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)
        # 列出当前文件夹下的所有文件和文件夹
        files = os.listdir(self.dir_path)
        # 遍历文件列表，找出以".txt"结尾的文件
        txt_files = [file for file in files if file.endswith(".txt")]
        # 输出结果
        self.lentxt = len(txt_files)
        print("当前文件夹下有%d个txt文件:" % self.lentxt)
        for txt_file in txt_files:
            print(txt_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建应用程序对象
    myWin = MyMainWindow()  # 实例化 MyMainWindow 类，创建主窗口
    myWin.show()  # 在桌面显示控件 myWin
    myWin.getSerialPort()  # 获取串口列表
    myWin.gettxtname()  # 获取创建的txt文档的名称

    sys.exit(app.exec_())  # 在主线程中退出
