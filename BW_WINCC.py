import sys
import json
import time
import serial
import serial.tools.list_ports
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtGui import QFont, QColor
from Ui_WINCC import Ui_MainWindow


class MyMainWindow(QMainWindow, Ui_MainWindow):  # 继承QMainWindow类和Ui_Maindow界面类
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)  # 初始化父类
        self.setupUi(self)  # 继承 Ui_MainWindow 界面类

    def getSerialPort(self):
        ports = serial.tools.list_ports.comports()
        if len(ports) == 0:
            self.comboBox_serial.addItem("-- 无串口 --")
            self.pushButton_connect.setEnabled(False)
        else:
            for port in reversed(ports):
                self.comboBox_serial.addItem(port.device)

    def connectSerial(self):
        self.ser = serial.Serial()
        select_port = self.comboBox_serial.currentText()  # 获取串口下拉列表值
        self.ser.port = select_port
        self.ser.baudrate = self.comboBox_baudrate.currentText()  # 获取波特率值
        self.ser.timeout = 5
        self.ser.open()
        print('seclect port is:', select_port)
        print('baudrate is:', self.ser.baudrate)
        # 串口连接按钮状态转换
        if self.pushButton_connect.text() == '连接串口':
            self.pushButton_connect.setText('已连接')
            self.pushButton_connect.setStyleSheet("background-color: yellow")
            self.comboBox_serial.setDisabled(True)
            self.comboBox_baudrate.setDisabled(True)
            print('serial port is open')
        else:
            self.pushButton_connect.setText('连接串口')
            self.pushButton_connect.setStyleSheet("background-color: none")
            self.comboBox_serial.setDisabled(False)
            self.comboBox_baudrate.setDisabled(False)
            self.ser.close()
            print('serial port is close')
        print('------------------------------')

    def refreshSerial(self):
        self.pushButton_connect.setEnabled(True)
        self.comboBox_serial.clear()
        myWin.getSerialPort()  # 获取串口列表
        if self.pushButton_connect.text() == '已连接':
            self.pushButton_connect.setText('连接串口')
            self.pushButton_connect.setStyleSheet("background-color: none")
            self.comboBox_serial.setDisabled(False)
            self.comboBox_baudrate.setDisabled(False)
            self.ser.close()
            print('serial port is close')
        print('refresh serial port')
        print('------------------------------')

    def trigger_actOpen(self):
        # 打开文件对话框
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'JSON Files (*.json)')
        if file_path:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)

            Cmdlist = []  # 指令保存列表
            self.widgetslist = [] # 组件列表
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
                layout.addWidget(labelName, item['id'], 0)
                # 自动保存widget为各个类型
                if item['widget'] == 'QLabel':
                    widget = QtWidgets.QLabel(self)
                    widget.setAlignment(QtCore.Qt.AlignCenter)
                    #if item['name'] == '序列号':
                        #widget.setObjectName('label_SN')
                    #    widget.setAlignment(QtCore.Qt.AlignCenter)
                    #elif item['name'] == '固件版本':
                        #widget.setObjectName('label_Version')
                    #    widget.setAlignment(QtCore.Qt.AlignCenter)
                    #elif item['name'] == '系统复位':
                        #widget.setObjectName('label_SystemReset')
                    #    widget.setAlignment(QtCore.Qt.AlignCenter)
                    #elif item['name'] == '单次触发指令':
                        #widget.setObjectName('label_SingleTrigger')
                    #    widget.setAlignment(QtCore.Qt.AlignCenter)
                    #elif item['name'] == '恢复出厂':
                        #widget.setObjectName('label_RestoreFactory')
                    #    widget.setAlignment(QtCore.Qt.AlignCenter)
                    #elif item['name'] == '保存':
                        #widget.setObjectName('label_Save')
                    #    widget.setAlignment(QtCore.Qt.AlignCenter)
                    layout.addWidget(widget, item['id'], 1)
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
                    elif item['name'] == 'I/O模式使能':
                        widget.addItems(['标准数据模式', '近高远低', '近低远高'])
                    else:
                        widget.setEditable(True)
                        widget.addItems(['option1', 'option2', 'option3'])
                    layout.addWidget(widget, item['id'], 1)
                elif item['widget'] == 'QLineEdit':
                    widget = QtWidgets.QLineEdit(self)
                    if item['name'] == '输出帧率':
                        widget.setObjectName('lineEdit_OutputFramerate')
                        widget.setPlaceholderText("1 - 1000 (Hz)")
                    elif item['name'] == '修改I2C从机地址':
                        widget.setObjectName('lineEdit_ChangeI2CAddress')
                        widget.setPlaceholderText("0x01 - 0x7F")
                    elif item['name'] == '低功耗模式使能':
                        widget.setObjectName('lineEdit_LowpowerEnable')
                        widget.setPlaceholderText("1 - 10 (Hz)")
                    layout.addWidget(widget, item['id'], 1)
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
            print('widgetslist:', self.widgetslist)
            print('buttonlist:', self.buttonlist)
            print('labelReturnlist:', self.labelReturnlist)
            print('------------------------------')
            self.widget1.setLayout(layout)
            # 连接指令按钮的点击信号和槽函数
            for button in self.buttonlist:
                button.clicked.connect(self.sendCmd)
            '''
            button = self.sender()  # 获取当前被点击的按钮
            index = self.buttonlist.index(button)  # 获取按钮在列表中的索引
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
        try:
            # self.ser.reset_input_buffer()

            button = self.sender()  # 获取当前被点击的按钮
            self.index = self.buttonlist.index(button)  # 获取按钮在列表中的索引
            if self.data[self.index]['widget'] == 'QLabel':
                cmd = self.data[self.index]['cmd']  # 获取对应的指令
                print('send cmd:', cmd)
                cmdb = bytes.fromhex(cmd)
                print('cmdb', cmdb)
                self.ser.reset_input_buffer()
                self.ser.write(cmdb)  # 发送指令
                print('------------------------------')
            elif self.data[self.index]['widget'] == 'QLineEdit':
                val = self.widgetslist[self.index].text()
                print(val)

            start_time = time.time()  # 记录开始时间
            while True:
                if self.ser.in_waiting:  # 如果串口有数据接收
                    rxhead = self.ser.read(1)  # 读取一个字节，作为帧头
                    print('rxhead:', rxhead, 'rxheadhex:', rxhead.hex())
                    if rxhead == b'Z' and self.data[self.index]['name'] != '单次触发指令':  # 判断帧头是否是0x5A
                        rxlen = self.ser.read(1)  # 若是读取一个长度字节
                        rxlenint = rxlen[0]  # 将bytes转为int
                        rxdata = self.ser.read(rxlenint - 2)  # 读取剩下的数据字节
                        self.rx = rxhead + rxlen + rxdata
                        print('rxlen', rxlen, 'rxdata:', rxdata, 'rx:', self.rx)
                        print('rxlenhex:', rxlen.hex(), 'rxlenint:', rxlenint, 'rxdatahex:', rxdata.hex())
                        print('rxhex:', ' '.join([hex(x)[2:].zfill(2) for x in self.rx]))
                        print('------------------------------')

                        self.labelReturnlist[self.index].setText('OK')  # 识别到帧头5A则回显标签OK
                        self.labelReturnlist[self.index].setStyleSheet('color: green')
                        break
                    elif self.data[self.index]['name'] == '单次触发指令':
                        print('判断帧率是否为零 若不是0则ng 是零则返回0字节数据帧')
                        break
                    else:
                        if (time.time() - start_time) > 2:  # 超过2s跳出循环
                            # QMessageBox.warning(self, '提示', '串口未打开或读取数据失败！')
                            break

            self.nameType()
        except Exception as e:
            print(e)
            self.labelReturnlist[self.index].setText('NG')
            self.labelReturnlist[self.index].setStyleSheet('color: red')
            # QMessageBox.warning(None, 'Error', str(e))
            # labelReturn.setText('NG')

    def nameType(self):
        if self.data[self.index]['name'] == '序列号':
            SN_rxhex = self.rx[3:17]
            SN_rxstr = ''.join([chr(x) for x in SN_rxhex])
            #SN_label = self.widget1.findChild(QtWidgets.QLabel, 'label_SN')
            #SN_label.setText(SN_rxstr)
            self.widgetslist[self.index].setText(SN_rxstr)
            print('序列号是：', SN_rxstr)
            print('------------------------------')
        elif self.data[self.index]['name'] == '固件版本':
            version_rxhex = self.rx[3:6][::-1].hex()  # 取出字节数组并反转后转为十六进制
            # 每两个字符由hex转为int，用'.'连接为str
            version_rxstr = '.'.join(str(int(version_rxhex[i:i + 2], 16)) for i in range(0, len(version_rxhex), 2))
            #version_label = self.widget1.findChild(QtWidgets.QLabel, 'label_Version')
            #version_label.setText(version_rxstr)
            self.widgetslist[self.index].setText(version_rxstr)
            print('固件版本是：', version_rxstr)
            print('------------------------------')
        elif self.data[self.index]['name'] == '系统复位':
            #systemreset_label = self.widget1.findChild(QtWidgets.QLabel, 'label_SystemReset')
            #systemreset_label.setText(' '.join([hex(x)[2:].zfill(2) for x in self.rx]))
            self.widgetslist[self.index].setText(' '.join([hex(x)[2:].zfill(2) for x in self.rx]))
            if self.rx.hex() != '5a05020061':
                self.labelReturnlist[self.index].setText('NG')
                self.labelReturnlist[self.index].setStyleSheet('color: red')
        elif self.data[self.index]['name'] == '恢复出厂':
            #restorefactory_label = self.widget1.findChild(QtWidgets.QLabel, 'label_RestoreFactory')
            #restorefactory_label.setText(' '.join([hex(x)[2:].zfill(2) for x in self.rx]))
            self.widgetslist[self.index].setText(' '.join([hex(x)[2:].zfill(2) for x in self.rx]))
            if self.rx.hex() != '5a0510006f':
                self.labelReturnlist[self.index].setText('NG')
                self.labelReturnlist[self.index].setStyleSheet('color: red')
        elif self.data[self.index]['name'] == '保存':
            #save_label = self.widget1.findChild(QtWidgets.QLabel, 'label_Save')
            #save_label.setText(' '.join([hex(x)[2:].zfill(2) for x in self.rx]))
            self.widgetslist[self.index].setText(' '.join([hex(x)[2:].zfill(2) for x in self.rx]))
            if self.rx.hex() != '5a05110070':
                self.labelReturnlist[self.index].setText('NG')
                self.labelReturnlist[self.index].setStyleSheet('color: red')
        elif self.data[self.index]['name'] == '输出帧率':
            outputframerate_edit = self.widget1.findChild(QtWidgets.QLineEdit, 'lineEdit_OutputFramerate')
            of_val = outputframerate_edit.text()
            of_hex = hex(of_val)
            print(of_hex)


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建应用程序对象
    myWin = MyMainWindow()  # 实例化 MyMainWindow 类，创建主窗口
    myWin.show()  # 在桌面显示控件 myWin
    myWin.getSerialPort()  # 获取串口列表
    # myWin.saveCmd()
    # myWin.sendCmd()
    sys.exit(app.exec_())  # 在主线程中退出
