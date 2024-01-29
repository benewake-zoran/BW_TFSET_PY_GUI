import time
import binascii
CMD_FRAME_HEADER = b'Z'  # 指令帧头定义 0x5A
RECV_FRAME_HEADER = b'YY'  # 接收数据帧头定义 0x59 0x59
DIS_DIFF = 10  # 允许测距误差范围
DIS_Cmd = '53 W 05 5A 05 00 01 60 50 53 R 09 50'  # IIC测距指令


# 通过轮询找到从机地址
def pollAddress_IIC(self):
    start_time = time.time()
    self.ser.reset_input_buffer()  # 清空输入缓存区
    for i in range(1, 128):
        Whex_i = hex((i << 1) & 0xFE)[2:].zfill(2).upper()  # 左移1位后最后位置0
        Rhex_i = hex((i << 1) | 0x01)[2:].zfill(2).upper()  # 左移1位后最后位置1
        NewCmd = DIS_Cmd.replace('W', Whex_i).replace('R', Rhex_i)
        print('i', i, '0xi:', hex(i)[2:].zfill(2), 'Whex_i:', Whex_i, 'Rhex_i:', Rhex_i, 'NewCmd:', NewCmd)
        self.ser.write(bytes.fromhex(NewCmd))
        time.sleep(0.05)  # 等待 50 ms
        if self.ser.in_waiting:
            rxIIC = self.ser.read(9)
            print('poll address rxIIC:', rxIIC.hex())
            if rxIIC[:2] == RECV_FRAME_HEADER:
                # self.address = hex(i)
                self.address = '0x{:02}'.format(hex(i)[2:].zfill(2).upper())
                self.rx = rxIIC
                self.IICCmd = NewCmd
                print('IIC address rx:', self.rx.hex())
                print('IIC address is:', '0x{:02}'.format(hex(i)[2:].zfill(2)).upper())
                if self.address is not None and self.rx != b'' and self.data[self.index]['name'] != '修改I2C从机地址' :
                   self.widgetslist[self.index].setText('HEX:'+self.address+' DEC:'+str(int(self.address, 16)))
                   self.labelReturnlist[self.index].setText('OK')
                   self.labelReturnlist[self.index].setStyleSheet('color: green')
                else:
                    self.labelReturnlist[self.index].setText('NG')
                    self.labelReturnlist[self.index].setStyleSheet('color: red')
                # self.ser.close()
                break
        else:
            self.rx = b''
            self.IICCmd = ''
            self.labelReturnlist[self.index].setText('NG')
            self.labelReturnlist[self.index].setStyleSheet('color: red')
    diff = time.time() - start_time
    print('diff:', diff)
    print('------------------------------')


# 若 JSON 文件有指令发送,则根据从机地址改写并发送指令
def sendCmd_IIC(self):
    if self.data[self.index]['widget'] == 'QLabel':
        print('common cmd:', self.data[self.index]['cmd'])  # 获取对应的指令
        if self.data[self.index]['cmd'] != '':  # 判断指令是否为空
            # 从机地址为空,进行轮询地址
            if self.address is None:
                print('when send cmd self.address is None')
                pollAddress_IIC(self)
            if self.address is not None:
                self.newCmd =  bytes.fromhex(self.data[self.index]['cmd'])
                sendDate(self)  #self.data
                
    elif self.data[self.index]['widget'] == 'QLineEdit':
        self.editVal = self.widgetslist[self.index].text()  # 获取文本框输入值  
        print('editVal:', self.editVal)
        lineEditCmd_IIC(self)
        self.ser.reset_input_buffer()
        sendDate(self)  #self.data
    elif self.data[self.index]['widget'] == 'QComboBox':
        self.boxVal = self.widgetslist[self.index].currentText()  # 获取当前下拉列表值  根据这个 选项 序号
        print('boxVal:', self.boxVal)
        comboBoxCmd(self)
        self.ser.reset_input_buffer()
        sendDate(self)  #self.data

def sendDate(self):
    Cmd = '53 W LEN1 DATA 50'  # IIC写操作
    Cmd1 = '53 R LEN2 50'      # IIC读操作
    DataCmd =   ' '.join([format(byte, '02X') for byte in self.newCmd])    # 计算后获得的5A开头的命令
    LEN1 = len(DataCmd.split())  # 计算写入指令字节数
    WCmd = hex((int(self.address, 16) << 1) & 0xFE)[2:].zfill(2).upper()  # 写操作
    RCmd = hex((int(self.address, 16) << 1) | 0x01)[2:].zfill(2).upper()  # 读操作
    NewCmd = Cmd.replace('W', WCmd).replace('LEN1', str(LEN1).zfill(2)).replace('DATA', DataCmd)
    NewCmd1 = Cmd1.replace('R', RCmd)
    if self.data[self.index]['name'] == '序列号' or self.data[self.index]['name'] == 'SerialNumber':
        NewCmd1 = NewCmd1.replace('LEN2', '12')
    elif self.data[self.index]['name'] == '固件版本' or self.data[self.index]['name'] == 'FirmwareVer':
        NewCmd1 = NewCmd1.replace('LEN2', '07')
    elif LEN1<5:
        NewCmd1 = NewCmd1.replace('LEN2', '05') #四字节长度如 保存
    else:
        NewCmd1 = NewCmd1.replace('LEN2', str(LEN1).zfill(2))  # 读取和发送数据一样的长度
    self.newCmd2 = bytes.fromhex(NewCmd)
    self.IICCmd = NewCmd  # IIC 指令 str类型
    self.newCmd1 = bytes.fromhex(NewCmd1)
    self.IICCmd1 = NewCmd1  # IIC 指令 str类型
    print('IIC 写指令:', self.IICCmd)
    print('IIC 读指令:', self.IICCmd1)
    self.ser.reset_input_buffer()
    self.ser.write(self.newCmd2)  # 发送写指令
    time.sleep(0.3)                
    self.ser.write(self.newCmd1)  # 发送读指令
    print('------------------------------')

# 发送指令后接收指令回显并判断 5A 帧头
def recvData_IIC(self):
    start_time = time.time()
    while True:
        if self.ser.in_waiting:
            rxhead = self.ser.read(1)  # 读取一个字节，作为帧头
            print('rxhead:', rxhead, 'rxheadhex:', rxhead.hex())
            if rxhead == CMD_FRAME_HEADER:  # 判断帧头是否是0x5A
                rxlen = self.ser.read(1)  # 若是读取一个长度字节
                rxlenint = rxlen[0]  # 将bytes转为int
                rxdata = self.ser.read(rxlenint - 2)  # 读取剩下的数据字节
                self.rx = rxhead + rxlen + rxdata
                print('rxlen', rxlen, 'rxdata:', rxdata, 'rx:', self.rx)
                print('rxlenhex:', rxlen.hex(), 'rxlenint:', rxlenint, 'rxdatahex:', rxdata.hex())
                print('rxhex:', ' '.join([hex(x)[2:].zfill(2) for x in self.rx]))
                break
            elif rxhead != CMD_FRAME_HEADER:  # 数据接收无帧头 5A 跳出循环
                print('rx head is not 5A')
                self.rx = rxhead + self.ser.readall()  # 读取串口所有数据来观察
                break
        elif (time.time() - start_time) > 3:  # 超过 3s 都无数据接收跳出循环
            print('time out 3s, try to poll address')
            pollAddress_IIC(self)  # 尝试再次轮询地址,看是否是发送指令的读写地址位错误
            sendCmd_IIC(self)  # 轮询地址后再次尝试发送指令
            time.sleep(0.5)
            if self.ser.in_waiting:
                rxhead = self.ser.read(1)
                print('rxhead:', rxhead.hex())
                # rxdata = self.ser.readall()
                if rxhead == CMD_FRAME_HEADER:  # 判断接收数据帧头是否为 5A
                    rxlen = self.ser.read(1)  # 若是读取一个长度字节
                    rxlenint = rxlen[0]  # 将bytes转为int
                    rxdata = self.ser.read(rxlenint - 2)  # 读取剩下的数据字节
                    self.rx = rxhead + rxlen + rxdata
                    print('poll again rx == head and rx:', self.rx.hex())
                    break
                elif rxhead != CMD_FRAME_HEADER:  # 数据接收无帧头 5A
                    self.rx = rxhead + self.ser.readall()  # 读取串口所有数据来观察
                    print('poll again rx != head and rx:', self.rx.hex())
                    break
            else:
                self.rx = b''
                print("poll again no rx")
                break
    print('------------------------------')


# 根据配置标签名称对rx进行处理和回显正误判断
def recvAnalysis_IIC(self):
    #第一种，发送固定，回显不定

    if self.data[self.index]['name'] == '序列号' or self.data[self.index]['name'] == 'SerialNumber':
        if self.rx != b'' and self.rx[2] == 0x12:
            SN_rxhex = self.rx[3:17]
            SN_rxstr = ''.join([chr(x) for x in SN_rxhex])
            self.widgetslist[self.index].setText(SN_rxstr)
            print('序列号是：', SN_rxstr)
            print('------------------------------')
        recvJudge_IIC(self)
    elif self.data[self.index]['name'] == '固件版本' or self.data[self.index]['name'] == 'FirmwareVer':
        if self.rx != b'' and self.rx[2] == 0x01:
            version_rxhex = self.rx[3:6][::-1].hex()  # 取出字节数组并反转后转为十六进制
            # 每两个字符由hex转为int，用'.'连接为str
            version_rxstr = '.'.join(str(int(version_rxhex[i:i + 2], 16)) for i in range(0, len(version_rxhex), 2))
            self.widgetslist[self.index].setText(version_rxstr)
            print('固件版本是：', version_rxstr)
            print('------------------------------')
        recvJudge_IIC(self)
    # else: #特殊的打印出相应信息，其他的要显示收到的消息
        
    #     self.widgetslist[self.index].setText(' '.join([hex(x)[2:].zfill(2) for x in self.rx]).upper())
        
    
    #第二类，一个发送对应多个结果，如保存对应成功或不成功
    
    if self.data[self.index]['name'] == '恢复出厂设置':
        if self.rx.hex() == '5a0510006f':  #
            self.labelReturnlist[self.index].setText('OK')  
            self.labelReturnlist[self.index].setStyleSheet('color: green')
        else :
            self.labelReturnlist[self.index].setText('NG')
            self.labelReturnlist[self.index].setStyleSheet('color: red')
    elif self.data[self.index]['name'] == '保存':
        if self.rx.hex() == '5a05110070':
            self.clearLabel() 
            self.labelReturnlist[self.index].setText('OK')  # 保存成功后
            self.labelReturnlist[self.index].setStyleSheet('color: green')
        else:
            self.labelReturnlist[self.index].setText('NG')
            self.labelReturnlist[self.index].setStyleSheet('color: red')
    elif self.data[self.index]['name'] == 'I/O模式使能':
        if self.rx.hex() == '5a053b009a':
            self.labelReturnlist[self.index].setText('OK')  # 保存成功后
            self.labelReturnlist[self.index].setStyleSheet('color: green')
        else :
            self.labelReturnlist[self.index].setText('NG')
            self.labelReturnlist[self.index].setStyleSheet('color:red')
    elif self.data[self.index]['name'] == '系统复位':  #实际上很难接收到数据
            self.clearLabel() 
    #第三类发什么收什么
    if (self.data[self.index]['name'] == '输出帧率' or self.data[self.index]['name'] == '输出模式' or self.data[self.index]['name'] == '输出开关' or 
            self.data[self.index]['name'] == '修改I2C从机地址' or self.data[self.index]['name'] == '低功耗模式' or self.data[self.index]['name'] == '强度低阈值和输出' or
            self.data[self.index]['name'] == '超低功耗模式' or self.data[self.index]['name'] == '单双频模式' or self.data[self.index]['name'] == '校验和开关' or
            self.data[self.index]['name'] == '配置120Ω端接电阻' or  self.data[self.index]['name'] == '低功耗模式设置'  or  self.data[self.index]['name'] == '波特率' or
             self.data[self.index]['name'] == '通信接口设置' ):
        if self.rx != self.newCmd: #回显和发送不一致
            print(self.rx)
            print(self.newCmd)
           
            self.labelReturnlist[self.index].setText('NG')
            self.labelReturnlist[self.index].setStyleSheet('color: red') 
        else:                      #回显和发送一致 
            self.labelReturnlist[self.index].setText('OK')  
            self.labelReturnlist[self.index].setStyleSheet('color: green')
   
           
            

        

#函数名：def recvJudge_IIC(self):
#功能：判断序列号测距等，发送之后接收的数据不确定的设置项是否成功。要有接收解析的新数据，才算成功
def recvJudge_IIC(self):
            if  self.widgetslist[self.index].text() != ''  and self.rx != b'':  
                self.labelReturnlist[self.index].setText('OK')
                self.labelReturnlist[self.index].setStyleSheet('color: green') 
            else :
                self.labelReturnlist[self.index].setText('NG')
                self.labelReturnlist[self.index].setStyleSheet('color: red')

# 通过轮询检查IIC从机地址
def checkAddress_IIC(self):
    pollAddress_IIC(self)  # 轮询地址
    if self.address is not None and self.rx != b'':
        self.widgetslist[self.index].setText(self.address)
    else:
        self.widgetslist[self.index].setText('')
    recvJudge_IIC(self)  # 判断期望值和检查值是否相同


# 检查测距
def checkDistance_IIC(self):
    if self.address is None:
        pollAddress_IIC(self)
        if self.rx != b'':
            dist = int.from_bytes(self.rx[2:4], byteorder='little')
            self.widgetslist[self.index].setText(str(dist) + ' (cm)')
    else:
        WCmd = hex((int(self.address, 16) << 1) & 0xFE)[2:].zfill(2).upper()  # 写操作
        RCmd = hex((int(self.address, 16) << 1) | 0x01)[2:].zfill(2).upper()  # 读操作
        NewCmd = DIS_Cmd.replace('W', WCmd).replace('R', RCmd)
        self.ser.write(bytes.fromhex(NewCmd))
        time.sleep(0.05)  # 等待 50 ms
        start_time = time.time()
        while True:
            if self.ser.in_waiting:
                rxIIC = self.ser.read(9)
                if rxIIC[:2] == RECV_FRAME_HEADER:
                    self.rx = rxIIC
                    self.IICCmd = NewCmd
                    print('IIC address rx:', self.rx.hex())
                    dist = int.from_bytes(self.rx[2:4], byteorder='little')
                    self.widgetslist[self.index].setText(str(dist) + ' (cm)')
                    break
            else:
                if (time.time() - start_time) > 1:
                    pollAddress_IIC(self)  # 尝试再次轮询地址,看是否是发送指令的读写地址位错误
                    if self.rx != b'':
                        dist = int.from_bytes(self.rx[2:4], byteorder='little')
                        self.widgetslist[self.index].setText(str(dist) + ' (cm)')
                    break
    print('------------------------------')
    recvJudge_IIC(self)


# 检查其他标签
def checkOther_IIC(self):
    if self.address is None:
        pollAddress_IIC(self)
        if self.rx != b'':
            dist = int.from_bytes(self.rx[2:4], byteorder='little')
            strength = int.from_bytes(self.rx[4:6], byteorder='little')
            temp = int.from_bytes(self.rx[6:8], byteorder='little')
            tempC = int(temp / 8 - 256)
            text = 'D=' + str(dist) + ';S=' + str(strength) + ';T=' + str(tempC)
            if self.data[self.index]['widget'] == 'QLabel':
                self.widgetslist[self.index].setText(text)
    else:
        WCmd = hex((int(self.address, 16) << 1) & 0xFE)[2:].zfill(2).upper()  # 写操作
        RCmd = hex((int(self.address, 16) << 1) | 0x01)[2:].zfill(2).upper()  # 读操作
        NewCmd = DIS_Cmd.replace('W', WCmd).replace('R', RCmd)
        self.ser.write(bytes.fromhex(NewCmd))
        time.sleep(0.05)  # 等待 50 ms
        start_time = time.time()
        while True:
            if self.ser.in_waiting:
                rxIIC = self.ser.read(9)
                if rxIIC[:2] == RECV_FRAME_HEADER:
                    self.rx = rxIIC
                    self.IICCmd = NewCmd
                    print('IIC address rx:', self.rx.hex())
                    dist = int.from_bytes(self.rx[2:4], byteorder='little')
                    strength = int.from_bytes(self.rx[4:6], byteorder='little')
                    temp = int.from_bytes(self.rx[6:8], byteorder='little')
                    tempC = int(temp / 8 - 256)
                    text = 'D=' + str(dist) + ';S=' + str(strength) + ';T=' + str(tempC)
                    if self.data[self.index]['widget'] == 'QLabel':
                        self.widgetslist[self.index].setText(text)
                    break
            else:
                if (time.time() - start_time) > 1:
                    pollAddress_IIC(self)  # 尝试再次轮询地址,看是否是发送指令的读写地址位错误
                    if self.rx != b'':
                        dist = int.from_bytes(self.rx[2:4], byteorder='little')
                        strength = int.from_bytes(self.rx[4:6], byteorder='little')
                        temp = int.from_bytes(self.rx[6:8], byteorder='little')
                        tempC = int(temp / 8 - 256)
                        text = 'D=' + str(dist) + ';S=' + str(strength) + ';T=' + str(tempC)
                        if self.data[self.index]['widget'] == 'QLabel':
                            self.widgetslist[self.index].setText(text)
                    break
    print('------------------------------')
    recvJudge_IIC(self)









def lineEditCmd_IIC(self):
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
    elif self.data[self.index]['name'] == '低功耗模式':
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



# 防止IIC转接板卡死
def refresh_IIC(self):
    if self.ser.rts is False:  # IIC转接板卡死复位
        self.ser.setRTS(True)
        self.ser.setRTS(False)
        rx = self.ser.read(2)
        if rx != b'':
            print(rx.hex())
