import sys
import json
import time
import os
import datetime
import serial
import serial.tools.list_ports
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtGui import QFont
from Ui_WINCC import Ui_MainWindow



class MyMainWindow(QMainWindow, Ui_MainWindow):  # 继承QMainWindow类和Ui_Maindow界面类
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)  # 初始化父类
        self.setupUi(self)  # 继承 Ui_MainWindow 界面类
        self.namelist = []  # 初始化点击按钮对应操作名称的列表
        self.vallist = []  # 初始化点击按钮对应显示值的列表
        self.returnlist = []  # 初始化点击按钮对应操作结果的列表
        self.cmdlist = []  # 初始化点击按钮对应发送指令的列表
        self.rxlist = []  # 初始化点击按钮对应接收指令的列表

    def getSerialPort(self):
        ports = serial.tools.list_ports.comports()
        if len(ports) == 0:
            self.comboBox_serial.addItem("-- 无串口 --")
            self.pushButton_connect.setEnabled(False)
        else:
            for port in reversed(ports):
                self.comboBox_serial.addItem(port.device)

    # 连接按钮的信号和槽函数
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

    # 刷新按钮的信号和槽函数
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

    # 菜单栏打开的信号和槽函数
    def trigger_actOpen(self):
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
                layout.addWidget(labelName, item['id'], 0)
                self.labellist.append(labelName)
                # 自动保存widget为各个类型
                if item['widget'] == 'QLabel':
                    widget = QtWidgets.QLabel(self)
                    widget.setAlignment(QtCore.Qt.AlignCenter)
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
                    else:
                        widget.setEditable(True)
                    layout.addWidget(widget, item['id'], 1)
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

    # 根据点击按钮的索引发送不同的指令
    def sendCmd(self):
        try:
            # self.ser.reset_input_buffer()

            button = self.sender()  # 获取当前被点击的按钮
            self.index = self.buttonlist.index(button)  # 获取按钮在列表中的索引
            if self.data[self.index]['widget'] == 'QLabel':
                labelCmd = self.data[self.index]['cmd']  # 获取对应的指令
                print('send cmd:', labelCmd)
                self.labelCmdb = bytes.fromhex(labelCmd)
                print('cmdb', self.labelCmdb)
                self.ser.reset_input_buffer()
                self.ser.write(self.labelCmdb)  # 发送指令
                print('------------------------------')
            elif self.data[self.index]['widget'] == 'QLineEdit':
                self.editVal = self.widgetslist[self.index].text()  # 获取文本框输入值
                print('editVal:', self.editVal)
                self.lineEditCmd()
                self.ser.reset_input_buffer()
                self.ser.write(self.newCmd)
            elif self.data[self.index]['widget'] == 'QComboBox':
                self.boxVal = self.widgetslist[self.index].currentText()  # 获取当前下拉列表值
                print('boxVal:', self.boxVal)
                self.comboBoxCmd()
                self.ser.reset_input_buffer()
                self.ser.write(self.newCmd)

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
                        start_time = time.time()  # 记录开始时间
                        start_frames = self.ser.in_waiting  # 记录开始时的数据帧数
                        time.sleep(1)  # 等待1秒
                        end_time = time.time()  # 记录结束时间
                        end_frames = self.ser.in_waiting  # 记录结束时的数据帧数
                        elapsed_time = end_time - start_time  # 计算经过的时间
                        frame_rate = (end_frames - start_frames) / elapsed_time  # 计算数据帧率
                        if frame_rate == 0:
                            rxdata = self.ser.read(8)  # 读取剩下字节
                            rx = rxhead + rxdata  # 连接帧头和数据段
                            self.rx = rx
                            print('rx:', ' '.join([hex(x)[2:].zfill(2) for x in rx]))
                            dist = int.from_bytes(rx[2:4], byteorder='little')
                            strength = int.from_bytes(rx[4:6], byteorder='little')
                            temp = int.from_bytes(rx[6:8], byteorder='little')
                            text = 'D=' + str(dist) + ';S=' + str(strength) + ';T=' + str(temp)
                            self.widgetslist[self.index].setText(text)
                            self.labelReturnlist[self.index].setText('OK')  # 帧率为0则回显标签OK
                            self.labelReturnlist[self.index].setStyleSheet('color: green')
                            print("Serial port output frame rate is 0.")
                        else:
                            self.rx = rxhead + self.ser.read(17)
                            self.widgetslist[self.index].setText('')
                            self.labelReturnlist[self.index].setText('NG')
                            self.labelReturnlist[self.index].setStyleSheet('color: red')
                            print("Serial port output frame rate is {}.".format(frame_rate))
                        break
                else:
                    if (time.time() - start_time) > 2:  # 超过2s跳出循环
                        # QMessageBox.warning(self, '提示', '串口未打开或读取数据失败！')
                        break

            self.nameType()
            self.savelist()
            self.saveSetting()

        except Exception as e:
            print(e)
            print(type(e))
            self.labelReturnlist[self.index].setText('NG')
            self.labelReturnlist[self.index].setStyleSheet('color: red')
            if type(e) == AttributeError or type(e) == serial.serialutil.PortNotOpenError:
                QMessageBox.warning(None, 'Error', '串口未连接或读取数据失败！')
            elif type(e) == ValueError or type(e) == IndexError:
                QMessageBox.warning(None, 'Error', '检查输入值！')
            else:
                QMessageBox.warning(None, 'Error', str(e))

    # 根据配置名称对rx进行处理和回显正误判断
    def nameType(self):
        if self.data[self.index]['name'] == '序列号':
            SN_rxhex = self.rx[3:17]
            SN_rxstr = ''.join([chr(x) for x in SN_rxhex])
            self.widgetslist[self.index].setText(SN_rxstr)
            print('序列号是：', SN_rxstr)
            print('------------------------------')
        elif self.data[self.index]['name'] == '固件版本':
            version_rxhex = self.rx[3:6][::-1].hex()  # 取出字节数组并反转后转为十六进制
            # 每两个字符由hex转为int，用'.'连接为str
            version_rxstr = '.'.join(str(int(version_rxhex[i:i + 2], 16)) for i in range(0, len(version_rxhex), 2))
            self.widgetslist[self.index].setText(version_rxstr)
            print('固件版本是：', version_rxstr)
            print('------------------------------')
        elif self.data[self.index]['name'] == '系统复位':
            self.widgetslist[self.index].setText(' '.join([hex(x)[2:].zfill(2) for x in self.rx]))
            if self.rx.hex() != '5a05020061':
                self.labelReturnlist[self.index].setText('NG')
                self.labelReturnlist[self.index].setStyleSheet('color: red')
        elif self.data[self.index]['name'] == '恢复出厂':
            self.widgetslist[self.index].setText(' '.join([hex(x)[2:].zfill(2) for x in self.rx]))
            if self.rx.hex() != '5a0510006f':
                self.labelReturnlist[self.index].setText('NG')
                self.labelReturnlist[self.index].setStyleSheet('color: red')
        elif self.data[self.index]['name'] == '保存':
            self.widgetslist[self.index].setText(' '.join([hex(x)[2:].zfill(2) for x in self.rx]))
            if self.rx.hex() != '5a05110070':
                self.labelReturnlist[self.index].setText('NG')
                self.labelReturnlist[self.index].setStyleSheet('color: red')
        elif (self.data[self.index]['name'] == '输出帧率' or self.data[self.index]['name'] == '输出模式' or self.data[self.index]['name'] == '波特率' or self.data[self.index]['name'] == '输出开关' or
              self.data[self.index]['name'] == '修改I2C从机地址' or self.data[self.index]['name'] == '低功耗模式使能' or self.data[self.index]['name'] == '强度低阈值和输出'):
            if self.rx != self.newCmd:
                self.labelReturnlist[self.index].setText('NG')
                self.labelReturnlist[self.index].setStyleSheet('color: red')
        elif self.data[self.index]['name'] == '通信接口设置':
            print('TF mini-S回显5a 05 0a 00 69;TF miniPlus 无回显')
            # if self.rx.hex() != '5a050a0069':
            #    self.labelReturnlist[self.index].setText('NG')
            #    self.labelReturnlist[self.index].setStyleSheet('color: red')
        elif self.data[self.index]['name'] == 'I/O模式使能':
            if self.rx.hex() != '5a053b009a':
                self.labelReturnlist[self.index].setText('NG')
                self.labelReturnlist[self.index].setStyleSheet('color:red')
        elif self.data[self.index]['widget'] == 'QLabel' and self.data[self.index]['name'] != '单次触发指令':
            self.widgetslist[self.index].setText(' '.join([hex(x)[2:].zfill(2) for x in self.rx]))

    # 根据QLineEdit组件的输入值得到对应的新指令
    def lineEditCmd(self):
        priCmd = self.data[self.index]['cmd']
        print('priCmd:', priCmd)
        priCmdhex_list = priCmd.split()  # 字符串存进一个列表
        priCmdhead_str = priCmdhex_list[0]  # 帧头
        priCmdlen_str = priCmdhex_list[1]  # 帧总长度
        priCmdid_str = priCmdhex_list[2]  # 帧功能码
        priCmddata_list = priCmdhex_list[3:-1]  # 帧数据段
        priCmdsum_int = int(priCmdhead_str, 16) + int(priCmdlen_str, 16) + int(priCmdid_str, 16)  # 未加数据段的校验和
        print('priCmddata_list:', priCmddata_list)

        if self.data[self.index]['name'] == '输出帧率':
            outframeVal_hexstr = hex(int(self.editVal))  # 将输入值转为十六进值字符串
            outframeVal_str = outframeVal_hexstr[2:]  # 将十六进制中的0x字符去掉
            outframeVal_str0 = outframeVal_str.rjust(4, '0')  # 补齐到4位不足添0
            outframeVal_list = [outframeVal_str0[i:i + 2] for i in range(0, len(outframeVal_str0), 2)]  # 每两个字符分割并存进列表
            print('outframeVal_list:', outframeVal_list)
            priCmddata_list[0] = outframeVal_list[1]  # 将输入低字节填入 LL 字符串
            priCmddata_list[1] = outframeVal_list[0]  # 将输入高字节填入 HH 字符串
            newCmddata_str = priCmddata_list[0] + priCmddata_list[1]  # 连接数据段
            newCmdsum_hexstr = hex(priCmdsum_int + int(outframeVal_list[0], 16) + int(outframeVal_list[1], 16))  # 加上数据段的校验和
        elif self.data[self.index]['name'] == '修改I2C从机地址':
            addrVal_hexstr = self.editVal  # 读取输入十六进制字符串
            print('addrVal_hexstr:', addrVal_hexstr)
            addrVal_str = addrVal_hexstr[2:]  # 将十六进制中的0x字符去掉
            priCmddata_list[0] = addrVal_str  # 填入ADDR字节
            newCmddata_str = priCmddata_list[0]
            newCmdsum_hexstr = hex(priCmdsum_int + int(addrVal_str, 16))  # 加上数据段的校验和
        elif self.data[self.index]['name'] == 'I/O模式使能':
            ioVal_list = self.editVal.split()  # 将输入值转为一个列表
            ioMODE_str = ioVal_list[0].rjust(2, '0')  # 将模式值转为十六进制字符串
            ioD_str = hex(int(ioVal_list[1]))[2:].rjust(4, '0')  # 将输入距离值转为十六进制字符串并去掉0x字符,且补齐到4位不足添0
            ioZone_str = hex(int(ioVal_list[2]))[2:].rjust(4, '0')  # 将输入滞回区间值转为十六进制字符串并去掉0x字符,且补齐到4位不足添0
            ioD_list = [ioD_str[i:i + 2] for i in range(0, len(ioD_str), 2)]  # 将输入距离值每两个字符分割并存进列表
            ioZone_list = [ioZone_str[i:i + 2] for i in range(0, len(ioZone_str), 2)]  # 将输入滞回区间值每两个字符分割并存进列表
            ioDL_str = ioD_list[1]  # 将距离低字节填入 DL 字符串
            ioDH_str = ioD_list[0]  # 将距离高字节填入 DH 字符串
            ioZoneL_str = ioZone_list[1]  # 将滞回区间低字节填入 ZoneL 字符串
            ioZoneH_str = ioZone_list[0]  # 将滞回区间高字节填入 ZoneH 字符串
            newCmddata_str = ioMODE_str + ioDL_str + ioDH_str + ioZoneL_str + ioZoneH_str  # 连接数据段
            newCmdsum_hexstr = hex(priCmdsum_int + int(ioMODE_str, 16) + int(ioDL_str, 16) + int(ioDH_str, 16) + int(ioZoneL_str, 16) + int(ioZoneH_str, 16))  # 加上数据段的校验和
        elif self.data[self.index]['name'] == '低功耗模式使能':
            lowpowVal_hexstr = hex(int(self.editVal))  # 将输入值转为十六进值字符串
            lowpowVal_str = lowpowVal_hexstr[2:]  # 将十六进制中的0x字符去掉
            lowpowVal_str0 = lowpowVal_str.rjust(2, '0')  # 补齐到2位不足添0
            priCmddata_list[0] = lowpowVal_str0  # 填入0X字节
            newCmddata_str = priCmddata_list[0] + priCmddata_list[1]  # 连接数据段
            newCmdsum_hexstr = hex(priCmdsum_int + int(lowpowVal_str0, 16))  # 加上数据段的校验和
        elif self.data[self.index]['name'] == '强度低阈值和输出':
            lowthresVal_list = self.editVal.split()  # 将输入值转为一个列表
            lowthresXX_str = hex(int(int(lowthresVal_list[0]) / 10))[2:].rjust(2, '0')  # 将输入强度值除10后转为十六进制字符串并去掉0x字符，且补齐到2位不足添0
            lowthresDis_str = hex(int(lowthresVal_list[1]))[2:].rjust(4, '0')  # 将输入距离值转为十六进制字符串并去掉0x字符,且补齐到4位不足添0
            lowthresDis_list = [lowthresDis_str[i: i + 2] for i in range(0, len(lowthresDis_str), 2)]  # 将输入距离值每两个字符分割并存进列表
            lowthresLL_str = lowthresDis_list[1]  # 将距离低字节填入 LL 字符串
            lowthresHH_str = lowthresDis_list[0]  # 将距离高字节填入 HH 字符串
            newCmddata_str = lowthresXX_str + lowthresLL_str + lowthresHH_str  # 连接数据段
            newCmdsum_hexstr = hex(priCmdsum_int + int(lowthresXX_str, 16) + int(lowthresLL_str, 16) + int(lowthresHH_str, 16))  # 加上数据段的校验和
        else:
            editVal_list = self.editVal.split()  # 将输入值转为一个列表
            for i in range(len(priCmddata_list)):
                priCmddata_list[i] = editVal_list[i]
                print(i, priCmddata_list[i], editVal_list[i])
            newCmddata_str = ''.join(editVal_list)
            print(newCmddata_str)
            newCmdsum_hexstr = hex(priCmdsum_int + sum(int(x, 16) for x in editVal_list))
            print(newCmdsum_hexstr)

        newCmdsum_str = str(newCmdsum_hexstr)[-2:]  # 取出校验和最后两位字符
        newCmdstr = priCmdhead_str + priCmdlen_str + priCmdid_str + newCmddata_str + newCmdsum_str  # 连接为更新后的指令字符串
        self.newCmd = bytes.fromhex(newCmdstr)  # 将指令字符串格式转为串口发送的字节格式
        print('newCmddata_str:', newCmddata_str)
        print('newCmdsum_hexstr:', newCmdsum_hexstr, 'newCmdsum_str:', newCmdsum_str)
        print('newCmdstr:', newCmdstr, 'newCmdbytes:', self.newCmd)
        print('------------------------------')

    # 根据QComboBox组件的输入值得到对应的新指令
    def comboBoxCmd(self):
        priCmd_list = self.data[self.index]['cmd']
        index = self.widgetslist[self.index].currentIndex()
        print('priCmd_list:', priCmd_list)
        if self.data[self.index]['name'] == '波特率':
            baudCmd_list = ['5A 08 06 80 25 00 00 0D', '5A 08 06 00 4B 00 00 B3', '5A 08 06 00 96 00 00 FE', '5A 08 06 00 E1 00 00 49',
                            '5A 08 06 00 C2 01 00 2B', '5A 08 06 00 E8 03 00 53', '5A 08 06 00 08 07 00 77', '5A 08 06 00 10 0E 00 86']
            comboboxCmd = baudCmd_list[index]
        else:
            comboboxCmd = priCmd_list[index]

        self.newCmd = bytes.fromhex(comboboxCmd)
        print('index:', index, 'comboboxCmd:', comboboxCmd, 'newCmdbytes:', self.newCmd)
        print('------------------------------')

    # 保存每次点击按钮收发的数据为列表
    def savelist(self):
        self.namelist.append(self.data[self.index]['name'])
        self.returnlist.append(self.labelReturnlist[self.index].text())
        self.rxlist.append(' '.join([hex(x)[2:].zfill(2) for x in self.rx]))
        if self.data[self.index]['widget'] == 'QLabel':
            # self.namelist.append(self.data[self.index]['name'])
            self.vallist.append(self.widgetslist[self.index].text())
            self.cmdlist.append(self.data[self.index]['cmd'])
        elif self.data[self.index]['widget'] == 'QLineEdit':
            # self.namelist.append(self.data[self.index]['name'])
            self.vallist.append(self.widgetslist[self.index].text())
            self.cmdlist.append(' '.join([hex(x)[2:].zfill(2) for x in self.newCmd]))
        elif self.data[self.index]['widget'] == 'QComboBox':
            # self.namelist.append(self.data[self.index]['name'])
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
    # myWin.saveCmd()
    # myWin.sendCmd()
    sys.exit(app.exec_())  # 在主线程中退出
