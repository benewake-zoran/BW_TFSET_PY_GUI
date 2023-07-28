import time


def send_UART(self):
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
        lineEditCmd_UART(self)
        self.ser.reset_input_buffer()
        self.ser.write(self.newCmd)
    elif self.data[self.index]['widget'] == 'QComboBox':
        self.boxVal = self.widgetslist[self.index].currentText()  # 获取当前下拉列表值
        print('boxVal:', self.boxVal)
        comboBoxCmd(self)
        self.ser.reset_input_buffer()
        self.ser.write(self.newCmd)


def recvData_UART(self):
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
            elif (time.time() - start_time) > 1:  # 超过1s跳出循环
                print('Timeout 1s, rx read 18 bytes')
                self.rx = self.ser.read(18)  # 读取两个帧来观察
                self.labelReturnlist[self.index].setText('NG')
                self.labelReturnlist[self.index].setStyleSheet('color: red')
                if self.data[self.index]['widget'] == 'QLabel':
                    self.widgetslist[self.index].setText('')
                if self.data[self.index]['name'] == '波特率':
                    self.baudrx = b''
                    self.labelReturnlist[self.index].setText('OK')
                    self.labelReturnlist[self.index].setStyleSheet('color: green')
                break
        else:
            if (time.time() - start_time) > 2:  # 超过2s跳出循环
                print('Timeout 1s, empty rx')
                self.rx = b''
                self.labelReturnlist[self.index].setText('NG')
                self.labelReturnlist[self.index].setStyleSheet('color: red')
                if self.data[self.index]['widget'] == 'QLabel':
                    self.widgetslist[self.index].setText('')
                # QMessageBox.warning(self, '提示', '串口未打开或读取数据失败！')
                break


def nameType_UART(self):
    if self.data[self.index]['name'] == '序列号':
        if self.rx[2] == 0x12:
            SN_rxhex = self.rx[3:17]
            SN_rxstr = ''.join([chr(x) for x in SN_rxhex])
            self.widgetslist[self.index].setText(SN_rxstr)
            print('序列号是：', SN_rxstr)
            print('------------------------------')
    elif self.data[self.index]['name'] == '固件版本':
        if self.rx[2] == 0x01:
            version_rxhex = self.rx[3:6][::-1].hex()  # 取出字节数组并反转后转为十六进制
            # 每两个字符由hex转为int，用'.'连接为str
            version_rxstr = '.'.join(str(int(version_rxhex[i:i + 2], 16)) for i in range(0, len(version_rxhex), 2))
            self.widgetslist[self.index].setText(version_rxstr)
            print('固件版本是：', version_rxstr)
            print('------------------------------')
    elif self.data[self.index]['name'] == '系统复位':
        self.widgetslist[self.index].setText(' '.join([hex(x)[2:].zfill(2) for x in self.rx]).upper())
        if self.rx.hex() != '5a05020061':
            self.labelReturnlist[self.index].setText('NG')
            self.labelReturnlist[self.index].setStyleSheet('color: red')
    elif self.data[self.index]['name'] == '恢复出厂':
        self.widgetslist[self.index].setText(' '.join([hex(x)[2:].zfill(2) for x in self.rx]).upper())
        if self.rx.hex() != '5a0510006f':
            self.labelReturnlist[self.index].setText('NG')
            self.labelReturnlist[self.index].setStyleSheet('color: red')
    elif self.data[self.index]['name'] == '保存':
        self.widgetslist[self.index].setText(' '.join([hex(x)[2:].zfill(2) for x in self.rx]).upper())
        if self.rx.hex() != '5a05110070':
            self.labelReturnlist[self.index].setText('NG')
            self.labelReturnlist[self.index].setStyleSheet('color: red')
    elif (self.data[self.index]['name'] == '输出帧率' or self.data[self.index]['name'] == '输出模式' or self.data[self.index]['name'] == '输出开关' or
            self.data[self.index]['name'] == '修改I2C从机地址' or self.data[self.index]['name'] == '低功耗模式使能' or self.data[self.index]['name'] == '强度低阈值和输出'):
        if self.rx != self.newCmd:
            self.labelReturnlist[self.index].setText('NG')
            self.labelReturnlist[self.index].setStyleSheet('color: red')
    elif self.data[self.index]['name'] == '波特率':
        if self.rx != self.newCmd and self.baudrx != b'':
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

def lineEditCmd_UART(self):
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

